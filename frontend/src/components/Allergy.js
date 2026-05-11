import React, { useState } from "react";
import "./Allergy.css";
import axios from "axios";
import { FaCheckCircle, FaSearch, FaUpload } from "react-icons/fa";

function Allergy() {
  const [symptoms, setSymptoms] = useState("");
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [foodResult, setFoodResult] = useState(null);
  const [search, setSearch] = useState("");
  const [registeredAllergies, setRegisteredAllergies] = useState([]);

  const defaultFoods = [
    "Milk",
    "Egg",
    "Peanut",
    "Seafood",
    "Wheat",
    "Soy",
    "Cheese",
    "Butter",
    "Chocolate",
    "Strawberry",
    "Fish",
    "Shrimp",
    "Chicken",
    "Fast Food",
  ];

  React.useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) return;

    axios
      .get("http://127.0.0.1:8000/api/dashboard/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        const allergyStr = res.data.allergies || "";
        const list = allergyStr.split(",").map((s) => s.trim()).filter((s) => s);
        setRegisteredAllergies(list);
      })
      .catch((err) => console.log(err));
  }, []);

  const foods = registeredAllergies.length > 0 ? registeredAllergies : defaultFoods;

  const handlePrediction = async () => {
    if (!symptoms && !image) {
      alert("Enter symptoms or upload image");
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      if (symptoms) {
        const list = symptoms.split(",").map((s) => s.trim());
        formData.append("symptoms", JSON.stringify(list));
      }
      if (image) formData.append("image", image);

      const res = await axios.post("http://127.0.0.1:8000/api/predict/", formData);
      setResult(res.data);
      setSelectedFoods([]);
      setFoodResult(null);
    } catch {
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const checkFoodAllergy = async () => {
    if (selectedFoods.length === 0) {
      alert("Select at least one food");
      return;
    }

    try {
      const token = localStorage.getItem("access");
      const res = await axios.post(
        "http://127.0.0.1:8000/api/predict/",
        {
          symptoms: symptoms ? symptoms.split(",") : [],
          meal_items: selectedFoods,
        },
        {
          headers: { Authorization: token ? `Bearer ${token}` : "" },
        }
      );
      setFoodResult(res.data);
    } catch {
      alert("Food check failed");
    }
  };

  const toggleFood = (food) => {
    setSelectedFoods((prev) =>
      prev.includes(food) ? prev.filter((f) => f !== food) : [...prev, food]
    );
  };

  const removeFood = (food) => {
    setSelectedFoods((prev) => prev.filter((f) => f !== food));
  };

  const filteredFoods = foods.filter((food) => food.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="allergy-page">
      <section className="allergy-intro surface-card">
        <div>
          <span className="page-kicker">Assessment input</span>
          <h3>Review symptoms, upload an image, and check food triggers.</h3>
          <p>
            The page keeps the assessment flow linear: provide input first, review prediction output next, then run a
            focused food-trigger check.
          </p>
        </div>
      </section>

      <div className="allergy-input-grid">
        <section className="allergy-card">
          <div className="allergy-card-header">
            <div>
              <h3>Symptoms</h3>
              <p>Enter symptoms as comma-separated values.</p>
            </div>
          </div>
          <textarea
            className="app-textarea"
            placeholder="e.g. rash, itching, sneezing"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
          />
        </section>

        <section className="allergy-card">
          <div className="allergy-card-header">
            <div>
              <h3>Image upload</h3>
              <p>Add a relevant skin image when available.</p>
            </div>
          </div>

          <label className="allergy-upload-box">
            <FaUpload className="upload-icon" />
            <span className="upload-title">{image ? image.name : "Upload skin image"}</span>
            <span className="upload-text">PNG or JPG input can be used with the symptom data.</span>
            <input type="file" hidden onChange={(e) => setImage(e.target.files[0])} />
          </label>
        </section>
      </div>

      <button type="button" className="app-button allergy-detect-btn" onClick={handlePrediction} disabled={loading}>
        {loading ? "Running assessment..." : "Run allergy assessment"}
      </button>

      {result && (
        <section className="allergy-result-section">
          <div className="result-header">
            <FaCheckCircle className="result-icon" />
            <div>
              <h2>Assessment result</h2>
              <p>Prediction output based on the submitted symptom and image data.</p>
            </div>
          </div>

          <div className="result-cards-grid">
            <article className="result-card">
              <h4>Predicted allergy</h4>
              <p className="result-value">{result.prediction}</p>
            </article>
            <article className="result-card">
              <h4>Risk level</h4>
              <p className="result-value">{result.risk}</p>
            </article>
            <article className="result-card">
              <h4>Confidence</h4>
              <p className="result-value">{result.confidence}%</p>
            </article>
          </div>

          <div className="food-selector-section">
            <div className="food-section-head">
              <div>
                <h3>Food trigger check</h3>
                <p>Select foods consumed recently to inspect potential triggers.</p>
              </div>
            </div>

            <div className="food-search-box">
              <FaSearch className="search-icon" />
              <input
                type="text"
                placeholder="Search food"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            {selectedFoods.length > 0 && (
              <div className="selected-food-tags">
                {selectedFoods.map((food) => (
                  <span key={food} className="food-tag">
                    {food}
                    <button type="button" className="tag-remove" onClick={() => removeFood(food)} aria-label={`Remove ${food}`}>
                      ×
                    </button>
                  </span>
                ))}
              </div>
            )}

            <div className="food-grid">
              {filteredFoods.map((food) => (
                <button
                  key={food}
                  type="button"
                  className={selectedFoods.includes(food) ? "food-btn selected" : "food-btn"}
                  onClick={() => toggleFood(food)}
                >
                  {food}
                </button>
              ))}
            </div>

            <button type="button" className="app-button check-food-btn" onClick={checkFoodAllergy} disabled={selectedFoods.length === 0}>
              Check selected foods
            </button>
          </div>

          {foodResult && (
            <div className="food-modal-overlay" onClick={() => setFoodResult(null)}>
              <div
                className={foodResult.food_allergy ? "food-modal allergy-detected" : "food-modal safe"}
                onClick={(e) => e.stopPropagation()}
              >
                <button type="button" className="modal-close-btn" onClick={() => setFoodResult(null)}>
                  ×
                </button>

                <div className="modal-header">
                  <h3>Food allergy analysis</h3>
                  <p>
                    {foodResult.food_allergy
                      ? "Potential trigger foods were detected from the selected items."
                      : "No immediate food triggers were detected from the selected items."}
                  </p>
                </div>

                {foodResult.food_allergy && foodResult.trigger_foods?.length > 0 && (
                  <div className="trigger-box">
                    <span className="trigger-label">Triggered foods</span>
                    <div className="trigger-items">
                      {foodResult.trigger_foods.map((food) => (
                        <span key={food} className="trigger-item">{food}</span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="modal-advice">
                  <h4>Recommendation</h4>
                  <p>
                    {foodResult.food_allergy
                      ? "Avoid the identified foods for now, monitor symptoms, and seek medical advice if reactions continue."
                      : "Continue monitoring your diet and seek medical advice if new symptoms appear."}
                  </p>
                </div>

                <button type="button" className="app-button modal-action-btn" onClick={() => setFoodResult(null)}>
                  Close result
                </button>
              </div>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

export default Allergy;
