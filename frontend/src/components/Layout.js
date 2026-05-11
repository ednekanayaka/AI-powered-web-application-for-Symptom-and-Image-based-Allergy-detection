import React, { useEffect, useState } from "react";
import { useNavigate, useLocation, Outlet } from "react-router-dom";
import axios from "axios";
import "./Layout.css";
import { decodeToken } from "../utils/auth";

import {
  FaAllergies,
  FaBars,
  FaBell,
  FaDumbbell,
  FaHome,
  FaMoon,
  FaSignOutAlt,
  FaSun,
  FaUtensils,
} from "react-icons/fa";

const PAGE_META = {
  "/dashboard": {
    title: "Dashboard",
    description: "Monitor your health summary, recent logs, and reminders.",
  },
  "/diet": {
    title: "Diet plans",
    description: "Review your personalized seven-day meal recommendations.",
  },
  "/exercise": {
    title: "Exercise plans",
    description: "Follow exercise guidance matched to your profile.",
  },
  "/allergy": {
    title: "Allergy detection",
    description: "Submit symptoms and images, then review risk and food-trigger checks.",
  },
};

function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [username, setUsername] = useState("User");

  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/");
  };

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/login");
      return;
    }

    const payload = decodeToken(token);
    if (payload?.is_admin) {
      navigate("/admin", { replace: true });
      return;
    }

    axios
      .get("http://127.0.0.1:8000/api/dashboard/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setUsername(res.data?.username || "User");
      })
      .catch((error) => {
        if (error.response?.status === 401) navigate("/");
      });

    axios
      .get("http://127.0.0.1:8000/api/notifications/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setNotifications(res.data || []);
      })
      .catch(() => {});
  }, [navigate]);

  const renderNavItem = (icon, label, path) => (
    <li
      className={location.pathname === path ? "active" : ""}
      onClick={() => {
        navigate(path);
        setSidebarOpen(false);
      }}
    >
      <div className="nav-link">
        <span className="nav-link-icon">{icon}</span>
        <span>{label}</span>
      </div>
    </li>
  );

  const pageMeta = PAGE_META[location.pathname] || PAGE_META["/dashboard"];

  return (
    <div className={darkMode ? "layout-wrapper dark" : "layout-wrapper"}>
      <button
        type="button"
        className={sidebarOpen ? "layout-overlay active" : "layout-overlay"}
        onClick={() => setSidebarOpen(false)}
        aria-label="Close navigation"
      />

      <aside className={sidebarOpen ? "layout-sidebar active" : "layout-sidebar"}>
        <div className="layout-sidebar-header">
          <button type="button" className="layout-logo" onClick={() => navigate("/dashboard")}>
            <span className="layout-logo-icon">HA</span>
            <span className="layout-logo-text">
              HealthAI
              <small>Patient workspace</small>
            </span>
          </button>
        </div>

        <ul className="layout-menu">
          {renderNavItem(<FaHome />, "Dashboard", "/dashboard")}
          {renderNavItem(<FaUtensils />, "Diet plans", "/diet")}
          {renderNavItem(<FaDumbbell />, "Exercise", "/exercise")}
          {renderNavItem(<FaAllergies />, "Allergy detection", "/allergy")}

          <li className="logout-item" onClick={handleLogout}>
            <div className="nav-link">
              <span className="nav-link-icon"><FaSignOutAlt /></span>
              <span>Logout</span>
            </div>
          </li>
        </ul>
      </aside>

      <div className="layout-main">
        <header className="layout-header">
          <div className="header-left">
            <button type="button" className="layout-menu-btn" onClick={() => setSidebarOpen(true)}>
              <FaBars />
            </button>
            <div>
              <div className="layout-header-kicker">Health workspace</div>
              <h2>{pageMeta.title}</h2>
              <p>{pageMeta.description}</p>
            </div>
          </div>

          <div className="header-actions">
            <button
              type="button"
              className="layout-notification"
              onClick={() => setShowNotifications((value) => !value)}
            >
              <FaBell />
              {notifications.length > 0 && <span className="layout-badge">{notifications.length}</span>}
            </button>

            <button type="button" className="layout-icon-btn" onClick={() => setDarkMode((value) => !value)}>
              {darkMode ? <FaSun /> : <FaMoon />}
            </button>

            <div className="layout-profile">
              <div className="profile-avatar">
                {username?.charAt(0)?.toUpperCase() || "U"}
              </div>
              <div className="profile-copy">
                <span className="profile-label">Signed in</span>
                <span className="profile-name">{username}</span>
              </div>
            </div>
          </div>

          {showNotifications && (
            <div className="layout-notification-panel">
              <div className="layout-notification-head">
                <h4>Notifications</h4>
                <span>{notifications.length}</span>
              </div>
              {notifications.length > 0 ? (
                notifications.slice(0, 5).map((note) => (
                  <div key={note.id} className="layout-notification-item">
                    <span>{note.message}</span>
                    <small>{note.created_at}</small>
                  </div>
                ))
              ) : (
                <div className="layout-notification-item">No new notifications.</div>
              )}
            </div>
          )}
        </header>

        <main className="layout-content">
          <Outlet context={{ darkMode, notifications }} />
        </main>
      </div>
    </div>
  );
}

export default Layout;
