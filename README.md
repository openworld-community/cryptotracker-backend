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
CREATE TABLE transactions (
  id AUTOINCREMENT PRIMARY KEY,
  sender_address text NOT NULL,
  receiving_address text NOT NULL,
  amount numeric(10,2) NOT NULL,
  currency text NOT NULL,
  status text NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
);
```