from fastapi import APIRouter
import requests

router = APIRouter()

TON_DEPOSIT_ADDRESS = ""

TON_API_KEY = ""
TON_API_ENDPOINT = "https://testnet.toncenter.com"


@router.get("/status_check")
async def status_check():
    return {"api_status_code": requests.get(f"{TON_API_ENDPOINT}").status_code}

async def retrieve_transactions():
    resp = requests.get(f'{TON_API_ENDPOINT}/api/v2/getTransactions?'
                        f'address={TON_DEPOSIT_ADDRESS}&limit=100&'
                        f'archival=true&api_key={TON_API_KEY}').json()

    return resp["result"] if resp['ok'] else []
