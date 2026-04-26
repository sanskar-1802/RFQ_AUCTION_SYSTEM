from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc
from datetime import datetime

from app.models import RFQ, Bid, AuctionLog
from app.schemas import RFQCreate
from app.deps import get_db

router = APIRouter(prefix="/rfq", tags=["RFQ"])


@router.post("/")
def create_rfq(data: RFQCreate, db: Session = Depends(get_db)):
    rfq = RFQ(
        name=data.name,
        bid_start_time=data.bid_start_time,
        bid_close_time=data.bid_close_time,
        current_bid_close_time=data.bid_close_time,
        forced_close_time=data.forced_close_time,
        trigger_window_minutes=data.trigger_window_minutes,
        extension_duration_minutes=data.extension_duration_minutes,
        extension_type=data.extension_type,
        status="ACTIVE"
    )

    db.add(rfq)
    db.commit()
    db.refresh(rfq)

    return rfq


@router.get("/")
def get_rfqs(db: Session = Depends(get_db)):
    rfqs = db.query(RFQ).all()
    result = []
    now = datetime.utcnow()

    for rfq in rfqs:

        
        if now >= rfq.forced_close_time:
            rfq.status = "FORCE_CLOSED"
        elif now >= rfq.current_bid_close_time:
            rfq.status = "CLOSED"
        else:
            rfq.status = "ACTIVE"

        
        lowest_bid = db.query(Bid).filter(Bid.rfq_id == rfq.id).order_by(asc(Bid.price)).first()

        result.append({
            "id": rfq.id,
            "name": rfq.name,
            "status": rfq.status,
            "current_bid_close_time": rfq.current_bid_close_time,
            "forced_close_time": rfq.forced_close_time,
            "lowest_bid": float(lowest_bid.price) if lowest_bid else None
        })

    db.commit()
    return result


@router.get("/{rfq_id}/details")
def get_rfq_details(rfq_id: int, db: Session = Depends(get_db)):
    rfq = db.query(RFQ).filter(RFQ.id == rfq_id).first()

    if not rfq:
        return {"error": "RFQ not found"}

    now = datetime.utcnow()

    
    if now >= rfq.forced_close_time:
        rfq.status = "FORCE_CLOSED"
    elif now >= rfq.current_bid_close_time:
        rfq.status = "CLOSED"
    else:
        rfq.status = "ACTIVE"

    bids = db.query(Bid).filter(Bid.rfq_id == rfq_id).order_by(asc(Bid.price)).all()
    logs = db.query(AuctionLog).filter(AuctionLog.rfq_id == rfq_id).all()

    ranked_bids = []
    for i, bid in enumerate(bids):
        ranked_bids.append({
            "supplier_id": bid.supplier_id,
            "price": float(bid.price),
            "rank": i + 1
        })

    db.commit()

    return {
        "rfq": {
            "id": rfq.id,
            "name": rfq.name,
            "status": rfq.status,
            "current_bid_close_time": rfq.current_bid_close_time,
            "forced_close_time": rfq.forced_close_time,
            "trigger_window_minutes": rfq.trigger_window_minutes,
            "extension_duration_minutes": rfq.extension_duration_minutes,
            "extension_type": rfq.extension_type
        },
        "bids": ranked_bids,
        "logs": logs
    }