from pydantic import BaseModel


class TransactionWaitingRequest(BaseModel):
    uid: int
    event_id: int
    amount: int
    transaction_type: str
    ttl: int = DEFAULT_TTL


class PendingTransaction(BaseModel):
    set_id: str