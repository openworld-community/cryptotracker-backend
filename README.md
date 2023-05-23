# cryptotracker-backend

Being tested. Functional still specifies to the event manager

## Setup

```cmd
python -m pip install -r requirements.txt
```

## Run

```cmd
uvicorn main:app --reload
```

## Usage

Route going on '/TICKER/add_pending_transaction'
Adds to the database a pending payment with its default TTL (to not overwhelm the DB).
Each tick, the Crypto APIs are called and the results of all transactions are added to the DB.
