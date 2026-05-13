import React, { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  CalendarRange,
  ShieldCheck,
  Stethoscope,
  UserPlus,
} from "lucide-react";
import { clearStoredTokens } from "../utils/auth";

function Register() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");
  const [fitnessGoal, setFitnessGoal] = useState("");
  const [allergies, setAllergies] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/api/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email,
          password,
          full_name: fullName,
          age,
          gender,
          height,
          weight,
          fitness_goal: fitnessGoal,
          allergies,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Account created successfully!");
        clearStoredTokens();
        navigate("/login?switch=1", { replace: true });
      } else {
        alert(data.error || "Registration failed");
      }
    } catch (error) {
      console.error("Registration error:", error);
      alert("Something went wrong with registration.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-shell">
        <aside className="auth-aside">
          <button type="button" className="auth-brand" onClick={() => navigate("/")}>
            <span className="auth-brand-mark">HA</span>
            <span>HealthAI</span>
          </button>

          <div className="auth-aside-copy">
            <span className="page-kicker">New account</span>
            <h1>Register once and keep your health profile connected to every screen.</h1>
            <p>
              The registration form collects the profile data needed for allergy-aware recommendations,
              fitness planning, and readable progress tracking across the system.
            </p>
          </div>

          <div className="auth-feature-list">
            <div className="auth-feature-item">
              <ShieldCheck size={18} />
              <div>
                <strong>Allergy-aware planning</strong>
                <span>Stored allergy preferences can inform later assessments and meal recommendations.</span>
              </div>
            </div>
            <div className="auth-feature-item">
              <CalendarRange size={18} />
              <div>
                <strong>Daily plan alignment</strong>
                <span>Height, weight, and fitness goal support more relevant diet and exercise guidance.</span>
              </div>
            </div>
            <div className="auth-feature-item">
              <Stethoscope size={18} />
              <div>
                <strong>Consistent follow-up</strong>
                <span>One account links assessment results, reminders, and ongoing progress logs.</span>
              </div>
            </div>
          </div>
        </aside>

        <section className="auth-panel">
          <div className="auth-card surface-card">
            <button type="button" className="auth-home-link" onClick={() => navigate("/")}>
              <ArrowLeft size={16} />
              Back to home
            </button>

            <div className="auth-card-header">
              <span className="page-kicker">Registration</span>
              <h2>Create your account</h2>
              <p>Complete both account details and health profile information.</p>
            </div>

            <form onSubmit={handleRegister} className="auth-form">
              <div className="auth-section-title">Account details</div>
              <div className="auth-form-grid">
                <div className="app-field">
                  <label htmlFor="register-name">Full name</label>
                  <input
                    id="register-name"
                    className="app-input"
                    type="text"
                    placeholder="Enter your name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                  />
                </div>

                <div className="app-field">
                  <label htmlFor="register-email">Email</label>
                  <input
                    id="register-email"
                    className="app-input"
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    autoComplete="username"
                    required
                  />
                </div>

                <div className="app-field full-width">
                  <label htmlFor="register-password">Password</label>
                  <input
                    id="register-password"
                    className="app-input"
                    type="password"
                    placeholder="Create a secure password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="new-password"
                    required
                  />
                </div>
              </div>

              <div className="auth-section-title">Health profile</div>
              <div className="auth-form-grid">
                <div className="app-field">
                  <label htmlFor="register-age">Age</label>
                  <input
                    id="register-age"
                    className="app-input"
                    type="number"
                    placeholder="Your age"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                  />
                </div>

                <div className="app-field">
                  <label htmlFor="register-gender">Gender</label>
                  <select
                    id="register-gender"
                    className="app-select"
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                  >
                    <option value="">Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div className="app-field">
                  <label htmlFor="register-height">Height (cm)</label>
                  <input
                    id="register-height"
                    className="app-input"
                    type="number"
                    placeholder="e.g. 170"
                    value={height}
                    onChange={(e) => setHeight(e.target.value)}
                  />
                </div>

                <div className="app-field">
                  <label htmlFor="register-weight">Weight (kg)</label>
                  <input
                    id="register-weight"
                    className="app-input"
                    type="number"
                    placeholder="e.g. 65"
                    value={weight}
                    onChange={(e) => setWeight(e.target.value)}
                  />
                </div>

                <div className="app-field">
                  <label htmlFor="register-goal">Fitness goal</label>
                  <select
                    id="register-goal"
                    className="app-select"
                    value={fitnessGoal}
                    onChange={(e) => setFitnessGoal(e.target.value)}
                  >
                    <option value="">Select goal</option>
                    <option value="general">General fitness</option>
                    <option value="lose weight">Lose weight</option>
                    <option value="gain muscle">Gain muscle</option>
                  </select>
                </div>

                <div className="app-field">
                  <label htmlFor="register-allergies">Known allergies</label>
                  <input
                    id="register-allergies"
                    className="app-input"
                    type="text"
                    placeholder="e.g. Dust, Milk"
                    value={allergies}
                    onChange={(e) => setAllergies(e.target.value)}
                  />
                </div>
              </div>

              <button type="submit" className="app-button auth-submit" disabled={loading}>
                {loading ? "Creating account..." : (
                  <>
                    <UserPlus size={16} />
                    Create account
                  </>
                )}
              </button>
            </form>

            <p className="auth-switch-row">
              Already registered?
              <button type="button" className="auth-switch-link" onClick={() => navigate("/login")}>
                Sign in
              </button>
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Register;
