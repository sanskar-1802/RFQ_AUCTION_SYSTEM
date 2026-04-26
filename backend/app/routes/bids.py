from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc
from datetime import datetime

from app.models import Bid, RFQ, AuctionLog, Supplier
from app.schemas import BidCreate
from app.deps import get_db
from app.services.auction_service import handle_auction_extension

router = APIRouter(prefix="/bids", tags=["Bids"])


@router.post("/")
def place_bid(data: BidCreate, db: Session = Depends(get_db)):
    rfq = db.query(RFQ).filter(RFQ.id == data.rfq_id).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")

    now = datetime.utcnow()

   
    if now >= rfq.forced_close_time:
        rfq.status = "FORCE_CLOSED"
        db.commit()
        raise HTTPException(status_code=400, detail="Auction force closed")

    if now >= rfq.current_bid_close_time:
        rfq.status = "CLOSED"
        db.commit()
        raise HTTPException(status_code=400, detail="Bidding time over")


    supplier = db.query(Supplier).filter(Supplier.id == data.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

 
    bid = Bid(
        rfq_id=data.rfq_id,
        supplier_id=data.supplier_id,
        price=data.price,
        created_at=datetime.utcnow()
    )
    db.add(bid)


    log = AuctionLog(
        rfq_id=data.rfq_id,
        event_type="BID",
        description=f"Supplier {data.supplier_id} placed bid {data.price}"
    )
    db.add(log)

    db.commit()

    handle_auction_extension(rfq, db)

    return {"message": "Bid placed successfully"}


@router.get("/{rfq_id}")
def get_bids(rfq_id: int, db: Session = Depends(get_db)):
    rfq = db.query(RFQ).filter(RFQ.id == rfq_id).first()

    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")

    now = datetime.utcnow()

  
    if now >= rfq.forced_close_time:
        rfq.status = "FORCE_CLOSED"
    elif now >= rfq.current_bid_close_time:
        rfq.status = "CLOSED"
    else:
        rfq.status = "ACTIVE"

    db.commit()

    bids = db.query(Bid).filter(Bid.rfq_id == rfq_id).order_by(asc(Bid.price)).all()

    response = []
    for i, bid in enumerate(bids):
        response.append({
            "id": bid.id,
            "supplier_id": bid.supplier_id,
            "price": float(bid.price),
            "rank": i + 1,
            "created_at": bid.created_at
        })

    return response