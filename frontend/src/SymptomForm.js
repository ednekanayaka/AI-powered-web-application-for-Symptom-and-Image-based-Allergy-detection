import React, { useState } from "react";

function SymptomForm() {
  const [symptoms, setSymptoms] = useState("");
  const [prediction, setPrediction] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!symptoms.trim()) {
      setPrediction("Please enter some symptoms");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/predict/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: symptoms.split(",") }),
      });

      if (!response.ok) {
        setPrediction("Error connecting to backend");
        return;
      }

      const data = await response.json();
      setPrediction(data.prediction || data.error);
    } catch (err) {
      setPrediction(
        `Backend unreachable. Frontend prediction: Predicted allergy based on: ${symptoms}`
      );
    }
  };

  return (
    <div style={{ margin: "50px" }}>
      <h2>Allergy Prediction</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter symptoms, comma separated"
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          style={{ width: "300px", padding: "5px" }}
        />
        <button type="submit" style={{ marginLeft: "10px" }}>
          Predict
        </button>
      </form>
      {prediction && <p>Prediction: {prediction}</p>}
    </div>
  );
}

export default SymptomForm;
