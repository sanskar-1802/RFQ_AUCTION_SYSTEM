from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class RFQ(Base):
    __tablename__ = "rfq"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    bid_start_time = Column(TIMESTAMP)
    bid_close_time = Column(TIMESTAMP)
    current_bid_close_time = Column(TIMESTAMP)
    forced_close_time = Column(TIMESTAMP)

    trigger_window_minutes = Column(Integer)
    extension_duration_minutes = Column(Integer)
    extension_type = Column(String)

    status = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    bids = relationship("Bid", back_populates="rfq")
    logs = relationship("AuctionLog", back_populates="rfq")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    bids = relationship("Bid", back_populates="supplier")


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)

    rfq_id = Column(Integer, ForeignKey("rfq.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

    price = Column(Numeric)
    rank = Column(Integer)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    rfq = relationship("RFQ", back_populates="bids")
    supplier = relationship("Supplier", back_populates="bids")


class AuctionLog(Base):
    __tablename__ = "auction_logs"

    id = Column(Integer, primary_key=True, index=True)

    rfq_id = Column(Integer, ForeignKey("rfq.id"))
    event_type = Column(String)
    description = Column(String)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    rfq = relationship("RFQ", back_populates="logs")