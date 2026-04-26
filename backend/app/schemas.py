from pydantic import BaseModel
from datetime import datetime


class RFQCreate(BaseModel):
    name: str
    bid_start_time: datetime
    bid_close_time: datetime
    forced_close_time: datetime
    trigger_window_minutes: int
    extension_duration_minutes: int
    extension_type: str


class SupplierCreate(BaseModel):
    name: str


class BidCreate(BaseModel):
    rfq_id: int
    supplier_id: int
    price: float