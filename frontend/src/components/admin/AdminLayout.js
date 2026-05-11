import React, { useState } from "react";
import { useNavigate, useLocation, Outlet } from "react-router-dom";
import {
  Dumbbell,
  LayoutDashboard,
  LogOut,
  Menu,
  Moon,
  Sun,
  Users,
  UtensilsCrossed,
} from "lucide-react";
import "../Layout.css";

const NAV = [
  { to: "/admin", label: "Dashboard", icon: <LayoutDashboard size={18} />, end: true },
  { to: "/admin/users", label: "Users", icon: <Users size={18} /> },
  { to: "/admin/diet", label: "Diet plans", icon: <UtensilsCrossed size={18} /> },
  { to: "/admin/exercise", label: "Exercises", icon: <Dumbbell size={18} /> },
];

const PAGE_META = {
  "/admin": {
    title: "Admin dashboard",
    description: "Monitor users and manage health-planning content.",
  },
  "/admin/users": {
    title: "Users",
    description: "Review registered accounts and remove records when necessary.",
  },
  "/admin/diet": {
    title: "Diet plan management",
    description: "Create, edit, and organize meal-plan entries.",
  },
  "/admin/exercise": {
    title: "Exercise management",
    description: "Maintain exercise guidance for each goal type.",
  },
};

function AdminLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/login");
  };

  const pageMeta = PAGE_META[location.pathname] || PAGE_META["/admin"];

  return (
    <div className={darkMode ? "layout-wrapper layout-admin dark" : "layout-wrapper layout-admin"}>
      <button
        type="button"
        className={sidebarOpen ? "layout-overlay active" : "layout-overlay"}
        onClick={() => setSidebarOpen(false)}
        aria-label="Close navigation"
      />

      <aside className={sidebarOpen ? "layout-sidebar active" : "layout-sidebar"}>
        <div className="layout-sidebar-header">
          <button type="button" className="layout-logo" onClick={() => navigate("/admin")}>
            <span className="layout-logo-icon">AD</span>
            <span className="layout-logo-text">
              HealthAI Admin
              <small>Management console</small>
            </span>
          </button>
        </div>

        <ul className="layout-menu">
          {NAV.map((item) => {
            const isActive = item.end
              ? location.pathname === item.to
              : location.pathname.startsWith(item.to);

            return (
              <li
                key={item.to}
                className={isActive ? "active" : ""}
                onClick={() => {
                  navigate(item.to);
                  setSidebarOpen(false);
                }}
              >
                <div className="nav-link">
                  <span className="nav-link-icon">{item.icon}</span>
                  <span>{item.label}</span>
                </div>
              </li>
            );
          })}

          <li className="logout-item" onClick={handleLogout}>
            <div className="nav-link">
              <span className="nav-link-icon"><LogOut size={18} /></span>
              <span>Logout</span>
            </div>
          </li>
        </ul>
      </aside>

      <div className="layout-main">
        <header className="layout-header">
          <div className="header-left">
            <button type="button" className="layout-menu-btn" onClick={() => setSidebarOpen(true)}>
              <Menu size={18} />
            </button>
            <div>
              <div className="layout-header-kicker">Administration</div>
              <h2>{pageMeta.title}</h2>
              <p>{pageMeta.description}</p>
            </div>
          </div>

          <div className="header-actions">
            <button type="button" className="layout-icon-btn" onClick={() => setDarkMode((value) => !value)}>
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
            </button>
            <div className="layout-profile">
              <div className="profile-avatar">A</div>
              <div className="profile-copy">
                <span className="profile-label">Role</span>
                <span className="profile-name">Administrator</span>
              </div>
            </div>
          </div>
        </header>

        <main className="layout-content">
          <Outlet context={{ darkMode }} />
        </main>
      </div>
    </div>
  );
}

export default AdminLayout;
