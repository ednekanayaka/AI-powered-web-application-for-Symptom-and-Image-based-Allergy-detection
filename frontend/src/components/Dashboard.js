import React, { useState, useEffect, useCallback } from "react";
import "./Dashboard.css";
import { useOutletContext, useNavigate } from "react-router-dom";
import axios from "axios";
import {
  Activity,
  AlertCircle,
  CheckCircle,
  ClipboardList,
  Flame,
  Timer,
} from "lucide-react";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const API = "http://127.0.0.1:8000/api";

function Dashboard() {
  const { notifications } = useOutletContext();
  const navigate = useNavigate();
  const [dataAPI, setDataAPI] = useState(null);
  const [checkin, setCheckin] = useState({ weight: "", exercise_minutes: "", calories: "" });
  const [checkinLoading, setCheckinLoading] = useState(false);
  const [checkinResult, setCheckinResult] = useState(null);

  const fetchDashboard = useCallback(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/");
      return;
    }

    axios
      .get(`${API}/dashboard/`, { headers: { Authorization: `Bearer ${token}` } })
      .then((res) => {
        setDataAPI(res.data);
        if (res.data?.weight) {
          setCheckin((prev) => ({ ...prev, weight: res.data.weight }));
        }
      })
      .catch((error) => {
        if (error.response?.status === 401) navigate("/");
      });
  }, [navigate]);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  const handleCheckin = async (e) => {
    e.preventDefault();
    if (!checkin.weight) {
      setCheckinResult({ success: false, message: "Weight is required." });
      return;
    }

    setCheckinLoading(true);
    setCheckinResult(null);

    try {
      const token = localStorage.getItem("access");
      const res = await axios.post(
        `${API}/daily-log/`,
        {
          weight: parseFloat(checkin.weight),
          exercise_minutes: checkin.exercise_minutes ? parseInt(checkin.exercise_minutes, 10) : null,
          calories: checkin.calories ? parseInt(checkin.calories, 10) : null,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setCheckinResult({
        success: true,
        message: `Logged successfully. BMI today: ${res.data.bmi}`,
      });

      fetchDashboard();
    } catch (err) {
      const msg = err.response?.data?.error || "Something went wrong.";
      setCheckinResult({ success: false, message: msg });
    } finally {
      setCheckinLoading(false);
    }
  };

  const chartData =
    dataAPI?.chart_data?.length > 1
      ? dataAPI.chart_data
      : [
          { day: "Start", value: dataAPI?.bmi || 0 },
          { day: "Today", value: dataAPI?.bmi || 0 },
        ];

  return (
    <div className="dashboard-container">
      <section className="dashboard-overview surface-card">
        <div>
          <span className="page-kicker">Health summary</span>
          <h3>Keep your profile, progress, and next actions in one view.</h3>
          <p>
            Review BMI, calories, exercise activity, recent logs, and reminders without leaving the dashboard.
          </p>
        </div>
        <div className="dashboard-overview-meta">
          <div>
            <span>Fitness goal</span>
            <strong>{dataAPI?.fitness_goal || "Not specified"}</strong>
          </div>
          <div>
            <span>Allergies</span>
            <strong>{dataAPI?.allergies || "None recorded"}</strong>
          </div>
        </div>
      </section>

      <section className="dashboard-stats">
        <article className="stat-card">
          <div className="stat-header">
            <div>
              <span className="stat-label">BMI</span>
              <h3>Body mass index</h3>
            </div>
            <span className="stat-icon"><Activity size={20} /></span>
          </div>
          <p className="stat-value">{dataAPI?.bmi || "Not set"}</p>
        </article>

        <article className="stat-card">
          <div className="stat-header">
            <div>
              <span className="stat-label">Calories</span>
              <h3>Latest intake</h3>
            </div>
            <span className="stat-icon"><Flame size={20} /></span>
          </div>
          <p className="stat-value">{dataAPI?.calories ? `${dataAPI.calories} kcal` : "--"}</p>
        </article>

        <article className="stat-card">
          <div className="stat-header">
            <div>
              <span className="stat-label">Exercise</span>
              <h3>Recorded activity</h3>
            </div>
            <span className="stat-icon"><Timer size={20} /></span>
          </div>
          <p className="stat-value">{dataAPI?.exercise ? `${dataAPI.exercise} min` : "--"}</p>
        </article>
      </section>

      <section className="dashboard-profile">
        <article className="profile-card">
          <span className="profile-card-label">Fitness goal</span>
          <strong>{dataAPI?.fitness_goal || "Not specified"}</strong>
        </article>
        <article className="profile-card">
          <span className="profile-card-label">Known allergies</span>
          <strong>{dataAPI?.allergies || "None"}</strong>
        </article>
        <article className="profile-card">
          <span className="profile-card-label">Weight / Height</span>
          <strong>
            {dataAPI?.weight ? `${dataAPI.weight} kg` : "--"} / {dataAPI?.height ? `${dataAPI.height} cm` : "--"}
          </strong>
        </article>
      </section>

      <section className="checkin-card">
        <div className="checkin-header">
          <div>
            <span className="page-kicker">Daily check-in</span>
            <h3>Log today&apos;s health data</h3>
          </div>
          <span className="app-status info">Dashboard update</span>
        </div>

        <form className="checkin-form" onSubmit={handleCheckin}>
          <div className="checkin-fields">
            <div className="app-field">
              <label htmlFor="checkin-weight">Weight (kg)</label>
              <input
                id="checkin-weight"
                className="app-input"
                type="number"
                step="0.1"
                min="20"
                max="300"
                placeholder="e.g. 72.5"
                value={checkin.weight}
                onChange={(e) => setCheckin({ ...checkin, weight: e.target.value })}
                required
              />
            </div>
            <div className="app-field">
              <label htmlFor="checkin-exercise">Exercise (minutes)</label>
              <input
                id="checkin-exercise"
                className="app-input"
                type="number"
                min="0"
                max="600"
                placeholder="e.g. 45"
                value={checkin.exercise_minutes}
                onChange={(e) => setCheckin({ ...checkin, exercise_minutes: e.target.value })}
              />
            </div>
            <div className="app-field">
              <label htmlFor="checkin-calories">Calories consumed</label>
              <input
                id="checkin-calories"
                className="app-input"
                type="number"
                min="0"
                max="10000"
                placeholder="e.g. 1800"
                value={checkin.calories}
                onChange={(e) => setCheckin({ ...checkin, calories: e.target.value })}
              />
            </div>
          </div>

          <button className="app-button checkin-btn" type="submit" disabled={checkinLoading}>
            <ClipboardList size={16} />
            {checkinLoading ? "Saving..." : "Update today's record"}
          </button>
        </form>

        {checkinResult && (
          <div className={`checkin-result ${checkinResult.success ? "success" : "error"}`}>
            {checkinResult.success ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
            <span>{checkinResult.message}</span>
          </div>
        )}
      </section>

      {dataAPI?.log_history?.length > 0 && (
        <section className="log-history-card">
          <div className="log-history-header">
            <div>
              <h3>Progress log</h3>
              <p>Recent measurements and daily activity entries.</p>
            </div>
            <span className="log-history-count">{dataAPI.log_history.length} entries</span>
          </div>

          <div className="log-history-table-wrap">
            <table className="log-history-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Weight</th>
                  <th>BMI</th>
                  <th>Exercise</th>
                  <th>Calories</th>
                </tr>
              </thead>
              <tbody>
                {dataAPI.log_history.map((entry, i) => (
                  <tr key={i}>
                    <td>{entry.date}</td>
                    <td className="log-time">{entry.time}</td>
                    <td>{entry.weight}</td>
                    <td>
                      <span
                        className={`bmi-tag ${
                          entry.bmi < 18.5
                            ? "bmi-under"
                            : entry.bmi < 25
                              ? "bmi-normal"
                              : entry.bmi < 30
                                ? "bmi-over"
                                : "bmi-obese"
                        }`}
                      >
                        {entry.bmi}
                      </span>
                    </td>
                    <td>{entry.exercise_minutes ?? "--"}</td>
                    <td>{entry.calories ?? "--"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      <section className="dashboard-lower">
        <article className="chart-container">
          <div className="chart-header">
            <div>
              <h3>BMI progress</h3>
              <p>Trend based on your stored daily logs.</p>
            </div>
          </div>

          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={chartData}>
              <CartesianGrid stroke="var(--border)" vertical={false} />
              <XAxis dataKey="day" stroke="var(--text-muted)" />
              <YAxis stroke="var(--text-muted)" domain={["auto", "auto"]} />
              <Tooltip
                contentStyle={{
                  background: "var(--bg-panel)",
                  border: "1px solid var(--border)",
                  borderRadius: "12px",
                  color: "var(--text-primary)",
                }}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#0f766e"
                strokeWidth={3}
                dot={{ fill: "#0f766e", r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </article>

        <article className="reminders-container">
          <div className="chart-header">
            <div>
              <h3>Reminders</h3>
              <p>Recent notifications from your account.</p>
            </div>
          </div>

          <div className="reminders-list">
            {notifications?.length > 0 ? (
              notifications.slice(0, 5).map((note, index) => (
                <div key={note.id || index} className="reminder-item">
                  <span className="reminder-dot" />
                  <p>{note.message}</p>
                </div>
              ))
            ) : (
              <div className="reminder-item">
                <span className="reminder-dot" />
                <p>Stay hydrated and continue your planned routine.</p>
              </div>
            )}
          </div>
        </article>
      </section>
    </div>
  );
}

export default Dashboard;
