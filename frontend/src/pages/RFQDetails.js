import { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import { getRFQDetails } from "../api/api";
import BidForm from "../components/BidForm";
import Timer from "../components/Timer";
import BidList from "../components/BidList";
import LogsList from "../components/LogsList";
import "../styles.css";

function RFQDetails() {
  const { id } = useParams();
  const [data, setData] = useState(null);

  const loadData = useCallback(() => {
    getRFQDetails(id).then(setData);
  }, [id]);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, [loadData]);

  if (!data) return <p>Loading...</p>;

  const isClosed =
    new Date(data.rfq.current_bid_close_time) < new Date() ||
    data.rfq.status !== "ACTIVE";

  return (
    <div className="container">
      <h2>{data.rfq.name}</h2>

    
      <p className="status">
        Status: <b>{data.rfq.status}</b>
      </p>

    
      <Timer endTime={data.rfq.current_bid_close_time} />

     
      <div className="config-box">
        <p>Trigger Window: {data.rfq.trigger_window_minutes} min</p>
        <p>Extension Duration: {data.rfq.extension_duration_minutes} min</p>
        <p>Extension Type: {data.rfq.extension_type}</p>
      </div>

      
      {isClosed ? (
        <p className="closed-text">🚫 Auction Closed</p>
      ) : (
        <BidForm rfqId={id} refresh={loadData} />
      )}


      <BidList bids={data.bids} />

    
      <LogsList logs={data.logs} />
    </div>
  );
}

export default RFQDetails;