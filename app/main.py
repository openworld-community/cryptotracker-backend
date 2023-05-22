import os
from pathlib import Path
import importlib

import asyncio
from fastapi import FastAPI, BackgroundTasks

from fastapi_utils.tasks import repeat_every
from logger import configure_logging
import logging
from database import Database


app = FastAPI()
db = Database()  # Initialize database connection


db.initialize_database()
configure_logging()

cogs_dir = Path("cogs")
for cog_file in cogs_dir.glob("*.py"):
    cog_module_name = cog_file.stem
    cog_module = importlib.import_module(f"cogs.{cog_module_name}")
    cog_router = cog_module.router
    app.include_router(cog_router, prefix=f"/{cog_module_name}")


@app.on_event("startup")
@repeat_every(seconds=60)
async def startup_event():
    db.remove_expired_transactions()
    logging.info("Ticker ticked")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)