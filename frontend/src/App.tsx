import { useState } from "react";
import "./App.css";

interface BackendResponse {
  question: string;
  status: "success" | "needs_clarification" | "error";
  clarification_question: string | null;
  sql: string;
  results: Record<string, any>[];
  error: string | null;
}

function App() {
  const [question, setQuestion] = useState("");
  const [sql, setSql] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [clarification, setClarification] = useState("");

  const askAI = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setClarification("");
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

      const data: BackendResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      if (data.status === "needs_clarification") {
        setClarification(data.clarification_question || "Please clarify your request.");
      } else if (data.status === "error") {
        setError(data.error || "An error occurred.");
      } else {
        setSql(data.sql);
        setResults(data.results || []);
      }
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
    setClarification("");
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

        {clarification && (
          <div className="warning" style={{ backgroundColor: '#fff3cd', color: '#856404', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
            🤔 <strong>Clarification Needed:</strong> {clarification}
          </div>
        )}

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