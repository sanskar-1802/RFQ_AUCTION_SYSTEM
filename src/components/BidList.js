function BidList({ bids }) {
  if (!bids || bids.length === 0) {
    return <p className="no-data">No bids yet</p>;
  }

  // ✅ Ensure sorted (safety)
  const sortedBids = [...bids].sort((a, b) => a.price - b.price);

  return (
    <div className="bid-container">
      <h3>📊 Bids</h3>

      <table className="bid-table">
        <thead>
          <tr>
            <th>Supplier</th>
            <th>Price</th>
            <th>Rank</th>
            <th>Time</th>
          </tr>
        </thead>

        <tbody>
          {sortedBids.map((bid) => (
            <tr
              key={bid.id || `${bid.supplier_id}-${bid.price}`}
              className={bid.rank === 1 ? "top-bid" : ""}
            >
              <td>Supplier {bid.supplier_id}</td>
              <td>₹ {bid.price}</td>
              <td>L{bid.rank}</td>
              <td>
                {bid.created_at
                  ? new Date(bid.created_at).toLocaleTimeString()
                  : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BidList;