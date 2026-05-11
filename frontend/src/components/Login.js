import React, { useEffect, useState } from "react";
import "./Login.css";

import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  CalendarRange,
  LogIn,
  ScanSearch,
  ShieldCheck,
} from "lucide-react";
import { decodeToken } from "../utils/auth";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (token) {
      const payload = decodeToken(token);
      if (payload?.is_admin) navigate("/admin", { replace: true });
      else navigate("/dashboard", { replace: true });
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        const payload = decodeToken(data.access);
        if (payload?.is_admin) navigate("/admin");
        else navigate("/dashboard");
      } else {
        alert(data.detail || "Invalid credentials");
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Something went wrong with login.");
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
            <span className="page-kicker">Secure access</span>
            <h1>Sign in to review assessments, plans, and daily logs.</h1>
            <p>
              The interface is built for readable health data, not visual noise.
              Return to your dashboard to check allergy predictions, meal guidance, exercise plans, and reminders.
            </p>
          </div>

          <div className="auth-feature-list">
            <div className="auth-feature-item">
              <ScanSearch size={18} />
              <div>
                <strong>Assessment results</strong>
                <span>Review symptom and image-based prediction output.</span>
              </div>
            </div>
            <div className="auth-feature-item">
              <CalendarRange size={18} />
              <div>
                <strong>Diet planning</strong>
                <span>Open seven-day meal guidance matched to your profile.</span>
              </div>
            </div>
            <div className="auth-feature-item">
              <ShieldCheck size={18} />
              <div>
                <strong>Progress tracking</strong>
                <span>Log weight, calories, exercise, and follow reminders.</span>
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
              <span className="page-kicker">Login</span>
              <h2>Welcome back</h2>
              <p>Use your registered account to access the health workspace.</p>
            </div>

            <form onSubmit={handleLogin} className="auth-form">
              <div className="app-field">
                <label htmlFor="login-email">Email address</label>
                <input
                  id="login-email"
                  className="app-input"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="username"
                  required
                />
              </div>

              <div className="app-field">
                <label htmlFor="login-password">Password</label>
                <input
                  id="login-password"
                  className="app-input"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                />
              </div>

              <button type="submit" className="app-button auth-submit" disabled={loading}>
                {loading ? "Signing in..." : (
                  <>
                    <LogIn size={16} />
                    Sign in
                  </>
                )}
              </button>
            </form>

            <p className="auth-switch-row">
              Need an account?
              <button type="button" className="auth-switch-link" onClick={() => navigate("/register")}>
                Create one
              </button>
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Login;
