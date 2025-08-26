import { useEffect, useState } from "react";

export default function App() {
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [location, setLocation] = useState("");
  const [recommendations, setRecommendations] = useState(null);
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
    <div className="container">
      <h1>Restaurant AI Group Picker</h1>

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

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Loading..." : "Get Recommendations"}
      </button>

      <div className="results">
        {recommendations &&
          recommendations.map((rec, idx) => (
            <div key={idx} className="recommendation">
              <h3>{rec.restaurant_name}</h3>
              <p>
                <strong>Public rating:</strong> {rec.public_rating} |{" "}
                <strong>Personal rating:</strong> {rec.personal_rating}
              </p>
              <p>{rec.description}</p>
              <p>
                <em>Reasoning: {rec.reccomendation_reasoning}</em>
              </p>
            </div>
          ))}
      </div>
    </div>
  );
}
