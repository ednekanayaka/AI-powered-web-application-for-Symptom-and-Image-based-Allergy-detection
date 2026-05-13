import React, { useState, useEffect } from "react";
import "./DietPlans.css";
import { useNavigate } from "react-router-dom";

const FALLBACK_MEAL_IMAGE = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80";

function DietPlans() {
  const navigate = useNavigate();
  const [dietData, setDietData] = useState([]);
  const [selectedDay, setSelectedDay] = useState(1);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/");
      return;
    }

    fetch("http://127.0.0.1:8000/api/diet/", {
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
        setDietData(data?.days || []);
      })
      .catch(() => {});
  }, [navigate]);

  const currentDayMeals = dietData.find((d) => d.day === selectedDay)?.meals || [];

  const handleImageError = (event) => {
    event.currentTarget.onerror = null;
    event.currentTarget.src = FALLBACK_MEAL_IMAGE;
  };

  return (
    <div className="diet-page">
      <section className="diet-intro surface-card">
        <div>
          <span className="page-kicker">Nutrition guidance</span>
          <h3>Your seven-day meal plan</h3>
          <p>
            Meal recommendations are organized by day and now keep allergy-matched meals visible with a clear safety label.
          </p>
        </div>
        <div className="diet-intro-badge">
          <span>Selected day</span>
          <strong>Day {selectedDay}</strong>
        </div>
      </section>

      <div className="days">
        {[1, 2, 3, 4, 5, 6, 7].map((num) => (
          <button
            key={num}
            type="button"
            className={selectedDay === num ? "day active" : "day"}
            onClick={() => setSelectedDay(num)}
          >
            Day {num}
          </button>
        ))}
      </div>

      <div className="diet-content">
        {currentDayMeals.length > 0 ? (
          currentDayMeals.map((meal, index) => (
            <article key={index} className="meal-card">
              <div className="meal-media">
                <img src={meal.image || FALLBACK_MEAL_IMAGE} alt={meal.name} onError={handleImageError} />
              </div>
              <div className="meal-text">
                <span className="meal-type-badge">{meal.title}</span>
                <h4>{meal.name}</h4>
                <div className="tags">
                  <span>{meal.calories} kcal</span>
                  <span>{meal.protein} protein</span>
                  <span className={meal.is_safe ? "safe" : "unsafe"}>
                    {meal.is_safe ? "Allergy aware" : "Not safe for your profile"}
                  </span>
                </div>
                {!meal.is_safe && meal.matched_allergies?.length > 0 && (
                  <p className="meal-warning">
                    Matches: {meal.matched_allergies.join(", ")}
                  </p>
                )}
              </div>
            </article>
          ))
        ) : (
          <div className="app-empty-state surface-card">
            <p>{dietData.length > 0 ? "No meals were found for this day." : "Loading your meal plan..."}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default DietPlans;
