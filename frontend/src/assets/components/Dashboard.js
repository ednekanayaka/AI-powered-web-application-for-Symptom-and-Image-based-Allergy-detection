import React from "react";
import "./Dashboard.css";

function Dashboard() {
  return (
    <div className="dashboard-container">

      {/* SIDEBAR */}
      <div className="sidebar">

        <h2 className="logo">
          AllergyCare
        </h2>

        <ul className="menu">

          <li>Dashboard</li>

          <li>Symptom Prediction</li>

          <li>Image Prediction</li>

          <li>History</li>

          <li>Logout</li>

        </ul>

      </div>

      {/* MAIN CONTENT */}
      <div className="main-content">

        <h1>
          Welcome to Allergy Detection System
        </h1>

        <p>
          Upload symptoms or images to predict allergies.
        </p>

        <div className="card-container">

          <div className="card">

            <h3>Symptom Prediction</h3>

            <p>
              Enter symptoms to detect possible allergies.
            </p>

            <button className="card-btn">
              Start Prediction
            </button>

          </div>

          <div className="card">

            <h3>Image Prediction</h3>

            <p>
              Upload skin image to detect allergies.
            </p>

            <button className="card-btn">
              Upload Image
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;