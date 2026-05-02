import { useEffect, useState } from "react";

function App() {
  const [health, setHealth] = useState("Loading...");
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState("");

  const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((res) => res.json())
      .then((data) => setHealth(data.status))
      .catch(() => setError("Cannot connect to backend health API"));

    fetch(`${API_BASE}/api/posts`)
      .then((res) => res.json())
      .then((data) => setPosts(data.posts || []))
      .catch(() => setError("Cannot connect to backend posts API"));
  }, [API_BASE]);

  return (
    <div style={{ padding: "30px", fontFamily: "Arial, sans-serif" }}>
      <h1>CMS Frontend</h1>
      <p>
        Backend health: <strong>{health}</strong>
      </p>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Posts</h2>
      {posts.length === 0 ? (
        <p>No posts found</p>
      ) : (
        <ul>
          {posts.map((post) => (
            <li key={post.id} style={{ marginBottom: "16px" }}>
              <h3>{post.title}</h3>
              <p>{post.content}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
