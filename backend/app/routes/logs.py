from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import AuctionLog
from app.deps import get_db

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/{rfq_id}")
def get_logs(rfq_id: int, db: Session = Depends(get_db)):
    return db.query(AuctionLog).filter(AuctionLog.rfq_id == rfq_id).all()