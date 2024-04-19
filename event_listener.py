from datetime import datetime
import logging
from typing import Dict, List, Optional
from web3 import Web3, HTTPProvider
from web3.contract import Contract

from config import CONTRACT_ABI, CONTRACT_ADDRESS, INFURA_URL
from db_manager import save_event_data, connect_db
from utils import format_duration, get_formatted_wei_amount

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize Web3 connection
web3 = Web3(HTTPProvider(INFURA_URL))
contract: Contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def handle_event(event: Dict) -> None:
    """
    Process and save data from a blockchain event.

    Args:
        event (Dict): The event data dictionary.
    """
    save_event_data(event, web3)

def get_events_from_last_24_hours() -> List[Dict]:
    """
    Retrieves blockchain events for 'TotalDistribution' from the last 24 hours.

    Returns:
        List[Dict]: List of event data dictionaries.
    """
    latest_block = web3.eth.block_number
    from_block = max(latest_block - 5760, 0)  # Assumes about 15 seconds per block

    event_filter = contract.events.TotalDistribution.createFilter(
        fromBlock=str(from_block),
        toBlock='latest'
    )
    events = event_filter.get_all_entries()
    return events

def add_new_event_to_db() -> None:
    """
    Retrieves new events and processes them to save in the database.
    """
    entries = get_events_from_last_24_hours()
    for event in entries:
        handle_event(event)

def generate_report() -> Optional[Dict]:
    """
    Generate a report from the database and calculate various statistics.

    Returns:
        Optional[Dict]: A dictionary containing the report data if successful, None otherwise.
    """
    try:
        conn = connect_db()
        cur = conn.cursor()
        sql_query = """
        SELECT
            MIN(time) AS first_tx_time,
            MAX(time) AS last_tx_time,
            SUM(input_aix_amount) AS total_input_aix_amount,
            SUM(distributed_aix_amount) AS total_distributed_aix_amount,
            SUM(swapped_eth_amount) AS total_swapped_eth_amount,
            SUM(distributed_eth_amount) AS total_distributed_eth_amount
        FROM
            total_distribution
        WHERE
            time >= NOW() - INTERVAL '24 HOURS';
        """
        cur.execute(sql_query)
        result = cur.fetchone()
        current_time = datetime.now()
        first_tx_ago = format_duration(current_time - result[0]) if result[0] else "No transactions"
        last_tx_ago = format_duration(current_time - result[1]) if result[1] else "No transactions"
        balance = web3.eth.getBalance("0x9A0A9594Aa626EE911207DC001f535c9eb590b34")
        eth_balance = web3.fromWei(balance, 'ether')
        report = {
            'first_tx': first_tx_ago,
            'last_tx': last_tx_ago,
            'aix_processed': get_formatted_wei_amount(result[2]) or 0,
            'aix_distributed': get_formatted_wei_amount(result[3]) or 0,
            'eth_bought': get_formatted_wei_amount(result[4]) or 0,
            'eth_distributed': get_formatted_wei_amount(result[5]) or 0,
            'eth_balance': round(eth_balance, 1),
        }
        
        return report
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        return None
    finally:
        cur.close()
        conn.close()
