import React, { useEffect, useState } from "react";
import { ArrowRight, Dumbbell, Users, UtensilsCrossed } from "lucide-react";
import "../Dashboard.css";
import "./Admin.css";
import { useNavigate } from "react-router-dom";

const API = "http://127.0.0.1:8000/api";
const headers = () => ({ Authorization: `Bearer ${localStorage.getItem("access")}` });

function AdminDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({ users: 0, meals: 0, exercises: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const [users, meals, exercises] = await Promise.all([
          fetch(`${API}/admin/users/`, { headers: headers() }).then((r) => r.json()),
          fetch(`${API}/admin/diet/`, { headers: headers() }).then((r) => r.json()),
          fetch(`${API}/admin/exercise/`, { headers: headers() }).then((r) => r.json()),
        ]);

        setStats({
          users: Array.isArray(users) ? users.filter((u) => !u.is_admin).length : 0,
          meals: Array.isArray(meals) ? meals.length : 0,
          exercises: Array.isArray(exercises) ? exercises.length : 0,
        });
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }

    fetchStats();
  }, []);

  const contentHealth = [
    {
      label: "User records",
      value: stats.users,
      tone: "blue",
      helper: "Registered non-admin accounts",
    },
    {
      label: "Meal plan coverage",
      value: stats.meals,
      tone: "green",
      helper: "Available diet plan entries",
    },
    {
      label: "Exercise coverage",
      value: stats.exercises,
      tone: "amber",
      helper: "Available exercise entries",
    },
  ];

  return (
    <div className="dashboard-container">
      <section className="dashboard-overview surface-card">
        <div>
          <span className="page-kicker">Admin overview</span>
          <h3>Manage accounts and health-planning content from one console.</h3>
          <p>Use the admin pages to maintain user records, meal plans, and exercise guidance without changing user-side flows.</p>
        </div>
      </section>

      {loading ? (
        <div className="app-empty-state surface-card">
          <p>Loading stats...</p>
        </div>
      ) : (
        <section className="dashboard-stats">
          <article className="stat-card">
            <div className="stat-header">
              <div>
                <span className="stat-label">Users</span>
                <h3>Registered accounts</h3>
              </div>
              <span className="stat-icon"><Users size={20} /></span>
            </div>
            <p className="stat-value">{stats.users}</p>
          </article>

          <article className="stat-card">
            <div className="stat-header">
              <div>
                <span className="stat-label">Diet plans</span>
                <h3>Meal entries</h3>
              </div>
              <span className="stat-icon"><UtensilsCrossed size={20} /></span>
            </div>
            <p className="stat-value">{stats.meals}</p>
          </article>

          <article className="stat-card">
            <div className="stat-header">
              <div>
                <span className="stat-label">Exercises</span>
                <h3>Exercise entries</h3>
              </div>
              <span className="stat-icon"><Dumbbell size={20} /></span>
            </div>
            <p className="stat-value">{stats.exercises}</p>
          </article>
        </section>
      )}

      <section className="admin-dashboard-grid">
        <article className="surface-card admin-panel-card">
          <div className="admin-panel-head">
            <div>
              <span className="page-kicker">Quick actions</span>
              <h3>Open the management area you need next.</h3>
            </div>
          </div>

          <div className="admin-quick-actions">
            <button type="button" className="admin-quick-action" onClick={() => navigate("/admin/users")}>
              <span className="admin-quick-icon"><Users size={18} /></span>
              <span className="admin-quick-copy">
                <strong>Manage users</strong>
                <small>Review account details and remove users when needed.</small>
              </span>
              <ArrowRight size={16} />
            </button>

            <button type="button" className="admin-quick-action" onClick={() => navigate("/admin/diet")}>
              <span className="admin-quick-icon"><UtensilsCrossed size={18} /></span>
              <span className="admin-quick-copy">
                <strong>Edit diet plans</strong>
                <small>Maintain meal entries by goal and day.</small>
              </span>
              <ArrowRight size={16} />
            </button>

            <button type="button" className="admin-quick-action" onClick={() => navigate("/admin/exercise")}>
              <span className="admin-quick-icon"><Dumbbell size={18} /></span>
              <span className="admin-quick-copy">
                <strong>Edit exercises</strong>
                <small>Adjust workout guidance for each goal type.</small>
              </span>
              <ArrowRight size={16} />
            </button>
          </div>
        </article>

        <article className="surface-card admin-panel-card">
          <div className="admin-panel-head">
            <div>
              <span className="page-kicker">System coverage</span>
              <h3>Check whether core admin content is populated.</h3>
            </div>
          </div>

          <div className="admin-coverage-list">
            {contentHealth.map((item) => (
              <div key={item.label} className="admin-coverage-item">
                <div className="admin-coverage-row">
                  <div>
                    <strong>{item.label}</strong>
                    <small>{item.helper}</small>
                  </div>
                  <span className={`admin-coverage-badge ${item.tone}`}>{item.value}</span>
                </div>
                <div className="admin-coverage-track">
                  <span
                    className={`admin-coverage-fill ${item.tone}`}
                    style={{ width: `${Math.min(100, Math.max(18, item.value * 4))}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>

    </div>
  );
}

export default AdminDashboard;
