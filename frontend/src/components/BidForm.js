import { useState } from "react";
import { placeBid } from "../api/api";

function BidForm({ rfqId, refresh }) {
  const [supplierId, setSupplierId] = useState("");
  const [price, setPrice] = useState("");

const handleSubmit = async () => {
  if (!supplierId || !price) {
    alert("Enter all fields");
    return;
  }

  await placeBid({
    rfq_id: parseInt(rfqId),
    supplier_id: parseInt(supplierId),
    price: parseFloat(price),
  });

  setPrice("");
  setSupplierId("");
  refresh();
};

  return (
    <div className="form">
      <input
        placeholder="Supplier ID"
        value={supplierId}
        onChange={(e) => setSupplierId(e.target.value)}
      />
      <input
        placeholder="Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
      />
      <button onClick={handleSubmit}>Place Bid</button>
    </div>
  );
}

export default BidForm;