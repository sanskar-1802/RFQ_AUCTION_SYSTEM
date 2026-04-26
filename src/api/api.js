const BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export const getRFQs = async () => {
  const res = await fetch(`${BASE_URL}/rfq/`);
  return res.json();
};

export const getRFQDetails = async (id) => {
  const res = await fetch(`${BASE_URL}/rfq/${id}/details`);
  return res.json();
};
export const placeBid = async (data) => {
  try {
    const res = await fetch("http://127.0.0.1:8000/bids/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await res.json();

    if (!res.ok) {
      throw new Error(result.detail || "Error placing bid");
    }

    return result;
  } catch (err) {
    console.error("BID ERROR:", err);
    alert(err.message);
  }
};