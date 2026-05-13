import React, { useState, useEffect } from "react";
import "./Exercise.css";
import { useNavigate } from "react-router-dom";
import { FaClock } from "react-icons/fa";

const FALLBACK_EXERCISE_IMAGE = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80";

function Exercise() {
  const navigate = useNavigate();
  const [exercises, setExercises] = useState([]);

  const handleImageError = (event) => {
    event.currentTarget.onerror = null;
    event.currentTarget.src = FALLBACK_EXERCISE_IMAGE;
  };

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/");
      return;
    }
    fetch("http://127.0.0.1:8000/api/exercise/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (res.status === 401) {
          navigate("/");
          throw new Error("Unauthorized");
        }
        return res.json();
      })
      .then((data) => {
        setExercises(data?.exercises || []);
      })
      .catch(() => {});
  }, [navigate]);

  return (
    <div className="exercise-page">
      <section className="exercise-intro surface-card">
        <div>
          <span className="page-kicker">Exercise guidance</span>
          <h3>Personalized exercise recommendations</h3>
          <p>Each plan card keeps the exercise name and duration visible without visual clutter.</p>
        </div>
      </section>

      <div className="exercise-grid">
        {exercises.length > 0 ? (
          exercises.map((item, index) => (
            <article className="exercise-card" key={index}>
              <div className="exercise-card-image">
                <img src={item.image || FALLBACK_EXERCISE_IMAGE} alt={item.name} onError={handleImageError} />
              </div>
              <div className="exercise-card-content">
                <h3>{item.name}</h3>
                <div className="exercise-meta">
                  <span className="duration-badge">
                    <FaClock />
                    {item.sets || "30 mins"}
                  </span>
                </div>
              </div>
            </article>
          ))
        ) : (
          <div className="app-empty-state surface-card">
            <p>Loading your personalized exercises...</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Exercise;
