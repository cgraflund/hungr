import { useEffect, useState } from "react";
import "./App.css"; // We'll create this CSS file

export default function App() {
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [location, setLocation] = useState("");

  useEffect(() => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setLocation(`${latitude},${longitude}`);
        },
        (error) => {
          console.error("Error fetching location:", error);
          setLocation("Denver, CO"); // fallback default
        }
      );
    } else {
      setLocation("Denver, CO"); // fallback if no geolocation
    }
  }, []);

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  // Load all users from backend
  useEffect(() => {
    fetch("http://localhost:8000/users")
      .then((res) => res.json())
      .then((data) => setUsers(data))
      .catch((err) => console.error("Error fetching users:", err));
  }, []);

  const toggleUser = (user) => {
    setSelectedUsers((prev) =>
      prev.includes(user) ? prev.filter((u) => u !== user) : [...prev, user]
    );
  };

  const handleSubmit = async () => {
    if (selectedUsers.length === 0 || !location) {
      alert("Please select at least one user and enter a location.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ users: selectedUsers, location }),
      });
      const data = await res.json();
      setRecommendations(data);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>🍽️ Restaurant AI Group Picker</h1>
        <p>Select friends and a location, and get the top restaurant recommendations!</p>
      </header>

      <section className="form-section">
        <div className="form-group">
          <label>Select Users:</label>
          <div className="checkbox-list">
            {users.map((user) => (
              <label key={user} className="checkbox-item">
                <input
                  type="checkbox"
                  checked={selectedUsers.includes(user)}
                  onChange={() => toggleUser(user)}
                />
                {user}
              </label>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Location (lat,lng):</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="39.745154503926216,-104.98128501283851"
          />
        </div>

        <button className="submit-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? "Loading..." : "Get Recommendations"}
        </button>
      </section>

      <section className="results-section">
        {recommendations.length > 0 && <h2>Top Recommendations</h2>}
        <div className="results-grid">
          {recommendations.map((rec, idx) => (
            <div key={idx} className="recommendation-card">
              <h3>{rec.restaurant_name}</h3>
              <p>
                <strong>Public rating:</strong> {rec.public_rating} |{" "}
                <strong>Personal rating:</strong> {rec.personal_rating}
              </p>
              <p>{rec.description}</p>
              <p className="reasoning">
                <em>Reasoning: {rec.reccomendation_reasoning}</em>
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
