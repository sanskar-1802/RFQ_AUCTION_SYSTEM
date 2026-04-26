import { useEffect, useState } from "react";

function Timer({ endTime }) {
  const [time, setTime] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const end = new Date(endTime);
      const diff = end - now;

      if (diff <= 0) {
        setTime("Auction Ended");
        clearInterval(interval); 
        return;
      }

      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);

      if (hours > 0) {
        setTime(`${hours}h ${minutes}m ${seconds}s`);
      } else {
        setTime(`${minutes}m ${seconds}s`);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [endTime]);

  return <h3>⏳ Time Left: {time}</h3>;
}

export default Timer;