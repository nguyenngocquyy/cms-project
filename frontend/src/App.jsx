import { useEffect, useState } from "react";
import "./App.css";

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000";

function App() {
  const [city, setCity] = useState("Hanoi");
  const [weather, setWeather] = useState(null);
  const [history, setHistory] = useState([]);
  const [health, setHealth] = useState("Loading...");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchHealth = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/health`);
      const data = await res.json();
      setHealth(data.status || "unknown");
    } catch (err) {
      setHealth("error");
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/history`);
      const data = await res.json();
      setHistory(data.history || []);
    } catch (err) {
      console.error("Cannot load history", err);
    }
  };

  const fetchWeather = async (searchCity) => {
    setLoading(true);
    setError("");

    try {
      const res = await fetch(
        `${API_BASE}/api/weather?city=${encodeURIComponent(searchCity)}`
      );

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to fetch weather");
      }

      const data = await res.json();
      setWeather(data);
      fetchHistory();
    } catch (err) {
      setError(err.message || "Cannot fetch weather");
      setWeather(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
    fetchHistory();
    fetchWeather("Hanoi");
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!city.trim()) return;
    fetchWeather(city.trim());
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="overlay">
          <div className="container">
            <p className="badge">Docker + ECR + EKS + Jenkins + Terraform</p>
            <h1>Weather Forecast App</h1>
            <p className="subtitle">
              Cloud-native weather application deployed on AWS with a full
              DevOps pipeline.
            </p>

            <div className="health-box">
              <strong>Backend health:</strong> {health}
            </div>

            <form className="search-form" onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Enter city name..."
                value={city}
                onChange={(e) => setCity(e.target.value)}
              />
              <button type="submit" disabled={loading}>
                {loading ? "Searching..." : "Search"}
              </button>
            </form>

            {error && <p className="error">{error}</p>}
          </div>
        </div>
      </header>

      <main className="container main-content">
        <section className="card weather-card">
          <h2>Current Weather</h2>

          {weather ? (
            <div className="weather-result">
              <div>
                <h3>
                  {weather.city}, {weather.country}
                </h3>
                <p className="temp">{weather.temperature}°C</p>
                <p className="desc">{weather.description}</p>
              </div>

              {weather.icon && (
                <img
                  className="weather-icon"
                  src={`https://openweathermap.org/img/wn/${weather.icon}@2x.png`}
                  alt={weather.description}
                />
              )}
            </div>
          ) : (
            <p>No weather data yet.</p>
          )}
        </section>

        <section className="grid-two">
          <div className="card">
            <h2>Project Overview</h2>
            <p>
              This project demonstrates an end-to-end DevOps workflow with a
              real weather application. The backend is built with Python,
              deployed with Docker, stored in Amazon ECR, orchestrated on Amazon
              EKS, automated by Jenkins, and provisioned with Terraform.
            </p>
          </div>

          <div className="card">
            <h2>Search History</h2>
            {history.length === 0 ? (
              <p>No search history yet.</p>
            ) : (
              <ul className="history-list">
                {history.map((item) => (
                  <li key={item.id}>
                    <strong>
                      {item.city}, {item.country}
                    </strong>
                    <span>{item.temperature}°C</span>
                    <small>{item.description}</small>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>

        <section className="grid-three">
          <div className="card">
            <h2>Tech Stack</h2>
            <ul className="simple-list">
              <li>React + Vite</li>
              <li>FastAPI + Python</li>
              <li>PostgreSQL</li>
              <li>Docker + Amazon ECR</li>
              <li>Amazon EKS</li>
              <li>Jenkins CI/CD</li>
              <li>Terraform</li>
            </ul>
          </div>

          <div className="card">
            <h2>Architecture</h2>
            <ul className="simple-list">
              <li>User → Frontend</li>
              <li>Frontend → Backend API</li>
              <li>Backend → OpenWeather API</li>
              <li>Backend → PostgreSQL</li>
              <li>Jenkins → Build & Deploy</li>
              <li>Terraform → Provision Infra</li>
            </ul>
          </div>

          <div className="card">
            <h2>CI/CD Flow</h2>
            <ul className="simple-list">
              <li>Push code to GitHub</li>
              <li>Jenkins pulls source</li>
              <li>Python deploy script runs</li>
              <li>Docker build + push ECR</li>
              <li>Deploy to EKS</li>
            </ul>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
