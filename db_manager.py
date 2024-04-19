import logging
from datetime import datetime
import psycopg2
from psycopg2.extensions import connection
from typing import Dict, Any

from web3 import Web3

from config import DATABASE_URL


logging.basicConfig(level=logging.INFO)

def connect_db() -> connection:
    """Establishes a connection to the database using the DATABASE_URL from the config."""
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

def create_table() -> None:
    """Creates a table for tracking total distributions if it doesn't already exist."""
    sql = """
        CREATE TABLE IF NOT EXISTS total_distribution (
            tx_hash VARCHAR(66) PRIMARY KEY,
            block_number INT,
            input_aix_amount NUMERIC,
            distributed_aix_amount NUMERIC,
            swapped_eth_amount NUMERIC,
            distributed_eth_amount NUMERIC,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    execute_sql(sql)

def execute_sql(sql: str, params: tuple = None) -> None:
    """Executes a given SQL command with optional parameters."""
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            conn.commit()

def save_event_data(event: Dict[str, Any], web3: Web3) -> None:
    """Saves event data to the database based on the event type."""
    transaction_hash = event['transactionHash'].hex()
    block = web3.eth.getBlock('latest')  # Simplified for demonstration; use actual block number if available
    transaction_time = datetime.utcfromtimestamp(block.timestamp)

    sql = """
        INSERT INTO total_distribution (
            tx_hash, block_number, input_aix_amount, distributed_aix_amount,
            swapped_eth_amount, distributed_eth_amount, time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (tx_hash) DO NOTHING;
    """
    params = (
        transaction_hash,
        event['blockNumber'],
        event['args']['inputAixAmount'],
        event['args']['distributedAixAmount'],
        event['args']['swappedEthAmount'],
        event['args']['distributedEthAmount'],
        transaction_time
    )
    execute_sql(sql, params)
