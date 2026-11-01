
import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [timestamps, setTimestamps] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleUpload() {
    if (!file) {
      setMessage("Please select a log file first.");
      return;
    }

    setLoading(true);
    setMessage("");
    setTimestamps([]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/extract",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      setTimestamps(data.timestamps);
      setMessage(data.message);
    } catch (error) {
      setMessage("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h1>Network Log Analyzer</h1>
      <p>Upload a network log file to extract timestamps.</p>

      <input
        type="file"
        accept=".txt,.log"
        onChange={(e) => {
          setFile(e.target.files[0] || null);
          setTimestamps([]);
          setMessage("");
        }}
      />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Extract Timestamps"}
      </button>

      {message && <p>{message}</p>}

      {timestamps.length > 0 && (
        <div className="results">
          <h2>Extracted Timestamps ({timestamps.length})</h2>
          <ul>
            {timestamps.map((timestamp, index) => (
              <li key={index}>{timestamp}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
