import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [sql, setSql] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askAI = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setSql("");
    setResults([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setSql(data.sql);
      setResults(data.results || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setQuestion("");
    setSql("");
    setResults([]);
    setError("");
  };

  return (
    <div className="app">
      <div className="container">

        <h1>🤖 AI Text-to-SQL Assistant</h1>

        <p className="subtitle">
          Ask questions about your database using natural language.
        </p>

        <div className="question-box">

          <textarea
            placeholder="Example: Show me students older than 20"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <div className="buttons">

            <button onClick={askAI} disabled={loading}>
              {loading ? "⏳ Asking AI..." : " Ask AI"}
            </button>

            <button className="clear-btn" onClick={clearAll}>
               Clear
            </button>

          </div>
        </div>

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

        {sql && (
          <div className="section">

            <h2>🧠 Generated SQL</h2>

            <pre>{sql}</pre>

          </div>
        )}

        {results.length > 0 && (
          <div className="section">

            <h2>📊 Results</h2>

            <div className="table-container">

              <table>

                <thead>
                  <tr>
                    {Object.keys(results[0]).map((key) => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>

                <tbody>

                  {results.map((row, index) => (
                    <tr key={index}>

                      {Object.values(row).map((value, i) => (
                        <td key={i}>{String(value)}</td>
                      ))}

                    </tr>
                  ))}

                </tbody>

              </table>

            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;