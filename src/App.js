import React, { useState } from "react"
import axios from "axios"
import "./App.css"

function SentimentAnalysis() {
  const [text, setText] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError("Please enter some text to analyze")
      return
    }

    setError(null)
    setLoading(true)

    try {
      const response = await axios.post("/predict", { text })
      setResult(response.data)
    } catch (error) {
      console.error("Error:", error)
      setError("Error connecting to the server. Please try again later.")
    } finally {
      setLoading(false)
    }
  }

  const getSentimentClass = () => {
    if (!result) return "neutral"
    const sentiment = result.prediction.toLowerCase()
    if (sentiment.includes("positive")) return "positive"
    if (sentiment.includes("negative")) return "negative"
    return "neutral"
  }

  return (
    <div className="container">
      <div className="centered">
        <h1 className="title">Tweet Sentiment Analysis</h1>
        <p className="description">
          Analyze the sentiment of any Tweet. Enter your content below and discover whether it conveys a positive,
          negative, or neutral tone.
        </p>
      </div>

      <div className="card">
        <textarea
          className="textarea"
          placeholder="Enter your text here..."
          rows={6}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        {error && <div className="alert">{error}</div>}

        <button onClick={handleAnalyze} disabled={loading} className="button">
          {loading ? "Analyzing..." : "Analyze Sentiment"}
        </button>
      </div>

      {result && (
        <div className={`result-card ${getSentimentClass()}`}>
          <div className="result-header">
            <div className={`icon ${getSentimentClass()}`}>
              {getSentimentClass() === "positive" ? "👍" : getSentimentClass() === "negative" ? "👎" : "➖"}
            </div>
            <div>
              <h2 className="title">Analysis Result</h2>
              <p className="description">Here's what we found about your text</p>
            </div>
          </div>
          <div className="result-content">
            <span className="text-slate-700">Sentiment:</span>
            <span className={`result-sentiment ${getSentimentClass()}`}>
              {result.prediction}
            </span>
          </div>
          <div className="result-footer">Based on our sentiment analysis algorithm</div>
        </div>
      )}
    </div>
  )
}

export default SentimentAnalysis
