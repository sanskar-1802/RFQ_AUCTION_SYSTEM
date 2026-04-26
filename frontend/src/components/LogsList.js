function LogsList({ logs }) {
  if (!logs || logs.length === 0) {
    return <p>No logs yet</p>;
  }

  return (
    <div>
      <h3>📝 Activity Logs</h3>
      <ul className="logs">
        {logs.map((log, index) => (
          <li key={index} className="log-item">
            <span className="log-time">
             {log.created_at
  ? new Date(log.created_at).toLocaleTimeString()
  : "—"}
            </span>
            {" - "}
            {log.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default LogsList;