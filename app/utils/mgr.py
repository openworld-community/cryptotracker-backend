import importlib
from pathlib import Path
import logging


cogs_dir = Path("cogs")

cogs_list = []

for cog_file in cogs_dir.glob("*.py"):
    cog_module_name = cog_file.stem
    if cog_module_name == "__init__":
        continue

    cog_module = importlib.import_module(f"cogs.{cog_module_name}")
    
    logging.info(f"Loaded cog: {cog_module_name}")

    cogs_list.append(cog_module)

async def call_all():
    for cog in cogs_list:
        logging.info(f"Calling cog: {cog.__name__}")
        logging.info(f"{await cog.process_transactions_from_api(await cog.retrieve_transactions_from_api())} transactions processed")