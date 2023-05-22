import asyncio
from fastapi import BackgroundTasks
from database import Database

import logging

db = Database()  # Initialize database connection

db.initialize_database()

async def tick():
    """
    Asynchronously runs an infinite loop checking for expired transactions in the database and
    removing them. 
    The function waits for 60 seconds after each loop before running the process again.
    """
    while True:
        db.remove_expired_transactions()
        logging.info("Ticker ticked")
        await asyncio.sleep(1)  # Sleep for 60 seconds before the next tick

def start_ticker(background_tasks: BackgroundTasks):
    logging.info("Ticker started")
    background_tasks.add_task(tick)
