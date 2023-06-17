from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from utils import database
from utils import models

from typing import Annotated
import requests
import logging


router = APIRouter()
db = database.Database()

TON_DEPOSIT_ADDRESS = "EQCqI4ITwXu0fAj1Y0B-FAD1bVh78dQTWh8vmEhVHJmOW0A2"
CURRENCY = "TON"
TON_API_KEY = "8248ac58bfc24d8e3731201f1ff2af5152ffde53134798158a984447150522ea"
TON_API_ENDPOINT = "https://testnet.toncenter.com"

DEFAULT_TTL = 10


class TransactionWaitingResponse(BaseModel):
    ok: bool


@router.get("/status_check")
async def status_check():
    return {"api_status_code": requests.get(f"{TON_API_ENDPOINT}").status_code}


@router.get("/transactions")
async def get_transactions(type: str = "processed"):
    return {"reply": db.get_transactions(currency=CURRENCY, type=_type)}


async def retrieve_transactions_from_api():
    logging.info("TON Retrieving transactions")

    resp = requests.get(
        f"{TON_API_ENDPOINT}/api/v2/getTransactions?"
        f"address={TON_DEPOSIT_ADDRESS}&limit=100&"
        f"archival=true&api_key={TON_API_KEY}"
    ).json()

    return resp["result"] if resp["ok"] else []


async def process_transactions_from_api(transactions):
    if transactions == []:
        return []

    existing_transactions_hashes = db.fetch_transaction_hashes()
    logging.info(
        f"""Processing {len(transactions)-len(existing_transactions_hashes)} new transactions"""
    )

    for transaction in transactions:
        if transaction["transaction_id"]["hash"] in existing_transactions_hashes:
            continue
        parsed = await parse_transaction(transaction)
        db.add_processed_transaction(
            parsed["currency"],
            parsed["amount"],
            parsed["transaction_hash"],
            parsed["timestamp"],
            parsed["from"],
            parsed["to"],
        )

    return len(transactions) - len(existing_transactions_hashes)


async def parse_comment(comment: str):
    return (
        {
                    "transaction_hash": comment,
                } if comment else None
    )


async def parse_transaction(transaction):
    return {
        "currency": CURRENCY,
        "amount": transaction["in_msg"]["value"],
        "timestamp": transaction["utime"],
        "transaction_hash": transaction["transaction_id"]["hash"],
        "from": transaction["in_msg"]["source"],
        "to": transaction["in_msg"]["destination"],
        "for_uid": transaction["in_msg"][""],
    }


@router.post(
    "/add_pending_transaction",
    status_code=201,
    response_description="Add transaction to pending queue",
    response_model=TransactionWaitingResponse,
)
async def add_pending_transaction(
    transaction_request: Annotated[
        TransactionWaitingRequest,
        Body(
            examples={
                "normal": {
                    "summary": "Adds a pending transaction and returns its internal transaction ID",
                    "description": "Adds a pending transaction of 2 TONs, which will be deleted after 10 ticks",
                    "value": {
                        "uid": 1111111111,
                        "event_id": 1,
                        "amount": 2000000000,
                        "ttl": 10,
                    },
                }
            }
        ),
    ]
):
    db.add_pending_transaction(
        CURRENCY, transaction_request.amount, transaction_request.ttl
    )
    return JSONResponse(status_code=201)  # TODO: add response model


@router.post("/force_process_transactions")
async def force_process_transactions():
    logging.info(msg="Force processing transactions")

    transactions = await retrieve_transactions_from_api()

    return {"processed_transactions": await process_transactions_from_api(transactions)}
