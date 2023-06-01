# cryptotracker-backend

Being tested. Functional still specifies to the event manager

## Setup

```cmd
python -m pip install -r requirements.txt
```

## Run

```cmd
cd app/
uvicorn main:app --reload
```

## Usage

Route going on '/TICKER/add_pending_transaction'
Adds to the database a pending payment with its default TTL (to not overwhelm the DB).
Each tick, the Crypto APIs are called and the results of all transactions are added to the DB.


## DB Reqs

```
CREATE TABLE crypto_processed_transactions (
  id AUTOINCREMENT PRIMARY KEY,
  sender_address TEXT NOT NULL,
  receiving_address TEXT NOT NULL,
  amount NUMERIC(10,24) NOT NULL,
  currency TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```

```
CREATE TABLE crypto_pending_transactions (
  id AUTOINCREMENT PRIMARY KEY,
  sender_address TEXT NOT NULL,
  receiving_address TEXT NOT NULL,
  amount NUMERIC(10,24) NOT NULL,
  currency TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```
