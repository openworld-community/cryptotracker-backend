import os
from pathlib import Path
import importlib
import asyncio
import logging
import uvicorn

from fastapi import FastAPI, BackgroundTasks
from fastapi_utils.tasks import repeat_every
from utils.logger import configure_logging
from utils.database import Database


TICK_INTERVAL = 60
TICK_COST = 1

app = FastAPI()
db = Database()  # Initialize database connection

db.initialize_database()
configure_logging()

cogs_dir = Path("cogs")
for cog_file in cogs_dir.glob("*.py"):
    cog_module_name = cog_file.stem
    if cog_module_name == "__init__":
        continue
    cog_module = importlib.import_module(f"cogs.{cog_module_name}")
    cog_router = cog_module.router
    app.include_router(cog_router, prefix=f"/{cog_module_name}")


from utils import mgr

@app.on_event("startup")
@repeat_every(seconds=TICK_INTERVAL)
async def ticker():

    logging.info("Manager calling all")
    await mgr.call_all()

    db.update_transactions_ttl(TICK_COST)
    db.remove_expired_transactions()
    logging.info("Ticker ticked")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)