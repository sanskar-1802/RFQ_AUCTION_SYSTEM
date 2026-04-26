import { useEffect, useState } from "react";
import { getRFQs } from "../api/api";
import { useNavigate } from "react-router-dom";
import "../styles.css";

function RFQList() {
  const [rfqs, setRfqs] = useState([]);
  const navigate = useNavigate();

useEffect(() => {
  getRFQs().then((data) => {
    if (Array.isArray(data)) {
      setRfqs(data);
    } else {
      console.error("Invalid response:", data);
      setRfqs([]);
    }
  });
}, []);

  return (
    <div className="container">
      <h1>🚀 RFQ Auctions</h1>
      <div className="card-grid">
        {rfqs.map((rfq) => (
<div key={rfq.id} className="card" onClick={() => navigate(`/rfq/${rfq.id}`)}>
  <h3>{rfq.name}</h3>
  <p>Status: {rfq.status}</p>
  <p>Lowest Bid: ₹ {rfq.lowest_bid || "N/A"}</p>
  <p>Close Time: {new Date(rfq.current_bid_close_time).toLocaleString()}</p>
  <p>Forced Close: {new Date(rfq.forced_close_time).toLocaleString()}</p>
</div>
        ))}
      </div>
    </div>
  );
}

export default RFQList;