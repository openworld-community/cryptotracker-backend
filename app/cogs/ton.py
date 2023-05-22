from fastapi import APIRouter
import requests

router = APIRouter()


TON_API_KEY = ""
TON_API_ENDPOINT = "https://testnet.toncenter.com"


@router.get("/status_check")
def example_route():
    return {"api_status_code": requests.get(f"{TON_API_ENDPOINT}").status_code}