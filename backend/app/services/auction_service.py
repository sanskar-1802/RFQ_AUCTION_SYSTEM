from datetime import datetime, timedelta
from sqlalchemy import asc
from app.models import Bid, AuctionLog

def handle_auction_extension(rfq, db):
    now = datetime.utcnow()
    trigger_time = rfq.current_bid_close_time - timedelta(minutes=rfq.trigger_window_minutes)

    if now < trigger_time:
        return

    bids = db.query(Bid).filter(Bid.rfq_id == rfq.id).order_by(asc(Bid.price)).all()

    if not bids:
        return

    should_extend = False
    latest_bid = bids[-1]

    if rfq.extension_type == "BID":
        should_extend = True

    elif rfq.extension_type == "RANK_CHANGE":
        if len(bids) > 1 and latest_bid.price < bids[-2].price:
            should_extend = True

    elif rfq.extension_type == "L1_CHANGE":
        if latest_bid.price == bids[0].price:
            should_extend = True

    if not should_extend:
        return

    new_time = rfq.current_bid_close_time + timedelta(minutes=rfq.extension_duration_minutes)

    if new_time > rfq.forced_close_time:
        new_time = rfq.forced_close_time

    if new_time > rfq.current_bid_close_time:
        rfq.current_bid_close_time = new_time

        log = AuctionLog(
            rfq_id=rfq.id,
            event_type="EXTENSION",
            description=f"Auction extended due to {rfq.extension_type} till {new_time}"
        )

        db.add(log)
        db.commit()