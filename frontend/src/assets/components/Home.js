import React from "react";
import "./Home.css";

function Home() {
  return (
    <div className="home-container">

      {/* NAVBAR */}
      <div className="navbar">
        <div className="menu-icon">☰</div>

        <div className="nav-links">
          <span>HOME</span>
          <span>ABOUT</span>
          <span>CONTACT</span>
        </div>

        <div className="nav-actions">
          <button className="nav-btn">Log In</button>
          <button className="nav-btn">Sign Up</button>
        </div>
      </div>

      {/* HERO SECTION */}
      <div className="hero">

        {/* LEFT TEXT */}
        <div className="hero-left">
          <h1>
            Your Personal AI <br />
            Health & Allergy <br />
            Manager
          </h1>

          <p>
            Track your meals, detect allergies, monitor your health,
            and receive AI-powered recommendations — all in one place.
          </p>

          <div className="hero-buttons">
            <button className="primary-btn">Get Started</button>
            <button className="secondary-btn">Learn More</button>
          </div>
        </div>

        {/* RIGHT IMAGE */}
        <div className="hero-right">
          <img
            src="/assets/runner.png"
            alt="Runner"
          />
        </div>

      </div>

    </div>
  );
}

export default Home;