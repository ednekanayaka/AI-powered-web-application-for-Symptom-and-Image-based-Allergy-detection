import React, { useEffect, useState } from "react";
import { Pencil, Plus, Trash2 } from "lucide-react";
import "./Admin.css";

const API = "http://127.0.0.1:8000/api";
const headers = () => ({ Authorization: `Bearer ${localStorage.getItem("access")}` });
const jsonHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem("access")}`,
  "Content-Type": "application/json",
});
const PAGE_SIZE = 8;

const EMPTY = { goal_type: "general", meal_type: "Breakfast", day: 1, name: "", calories: "", protein: "", image_url: "" };

function AdminDiet() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(null);
  const [form, setForm] = useState(EMPTY);
  const [editId, setEditId] = useState(null);
  const [filterGoal, setFilterGoal] = useState("all");
  const [page, setPage] = useState(1);

  const fetchPlans = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/admin/diet/`, { headers: headers() });
      const data = await res.json();
      setPlans(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlans();
  }, []);

  const openAdd = () => {
    setForm(EMPTY);
    setEditId(null);
    setModal("add");
  };

  const openEdit = (p) => {
    setForm({ ...p });
    setEditId(p.id);
    setModal("edit");
  };

  const closeModal = () => setModal(null);

  const handleSave = async () => {
    const body = JSON.stringify({ ...form, calories: Number(form.calories), day: Number(form.day) });
    if (modal === "add") {
      await fetch(`${API}/admin/diet/`, { method: "POST", headers: jsonHeaders(), body });
    } else {
      await fetch(`${API}/admin/diet/${editId}/`, { method: "PUT", headers: jsonHeaders(), body });
    }
    closeModal();
    fetchPlans();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this meal plan entry?")) return;
    await fetch(`${API}/admin/diet/${id}/`, { method: "DELETE", headers: headers() });
    setPlans((prev) => prev.filter((p) => p.id !== id));
  };

  const filtered = filterGoal === "all" ? plans : plans.filter((p) => p.goal_type === filterGoal);
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  useEffect(() => {
    setPage(1);
  }, [filterGoal]);

  useEffect(() => {
    if (page > totalPages) setPage(totalPages);
  }, [page, totalPages]);

  return (
    <div className="dashboard-container">
      <section className="log-history-card">
        <div className="log-history-header">
          <div>
            <h3>Diet plan entries</h3>
            <p>{filtered.length} items shown for the selected filter.</p>
          </div>

          <div className="admin-toolbar-actions">
            <select className="app-select admin-select" value={filterGoal} onChange={(e) => setFilterGoal(e.target.value)}>
              <option value="all">All goals</option>
              <option value="general">General</option>
              <option value="muscle">Muscle gain</option>
              <option value="lose">Weight loss</option>
            </select>
            <button type="button" className="app-button admin-inline-btn" onClick={openAdd}>
              <Plus size={14} />
              Add meal
            </button>
          </div>
        </div>

        {loading ? (
          <div className="app-empty-state">
            <p>Loading meal plans...</p>
          </div>
        ) : filtered.length === 0 ? (
          <div className="app-empty-state">
            <p>No meal plans found.</p>
          </div>
        ) : (
          <div className="log-history-table-wrap">
            <table className="log-history-table">
              <thead>
                <tr>
                  <th className="col-role">Goal</th>
                  <th className="col-id">Day</th>
                  <th>Meal type</th>
                  <th>Name</th>
                  <th className="col-id">Calories</th>
                  <th className="col-role">Protein</th>
                  <th className="col-actions">Actions</th>
                </tr>
              </thead>
              <tbody>
                {paginated.map((p) => (
                  <tr key={p.id}>
                    <td className="cell-center"><span className={`admin-badge admin-goal-${p.goal_type}`}>{p.goal_type}</span></td>
                    <td className="cell-strong">Day {p.day}</td>
                    <td>{p.meal_type}</td>
                    <td className="cell-wrap">{p.name}</td>
                    <td>{p.calories} kcal</td>
                    <td>{p.protein}</td>
                    <td className="admin-action-cell">
                      <button type="button" className="app-button-secondary admin-inline-btn" onClick={() => openEdit(p)}>
                        <Pencil size={14} />
                        Edit
                      </button>
                      <button type="button" className="app-button-danger admin-inline-btn" onClick={() => handleDelete(p.id)}>
                        <Trash2 size={14} />
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {!loading && filtered.length > 0 && (
          <div className="admin-pagination">
            <span>Page {page} of {totalPages}</span>
            <div className="admin-pagination-actions">
              <button type="button" className="app-button-secondary" disabled={page === 1} onClick={() => setPage((value) => value - 1)}>
                Previous
              </button>
              <button type="button" className="app-button-secondary" disabled={page === totalPages} onClick={() => setPage((value) => value + 1)}>
                Next
              </button>
            </div>
          </div>
        )}
      </section>

      {modal && (
        <div className="admin-modal-overlay" onClick={closeModal}>
          <div className="admin-modal" onClick={(e) => e.stopPropagation()}>
            <h3>{modal === "add" ? "Add meal plan" : "Edit meal plan"}</h3>

            <div className="app-field">
              <label htmlFor="diet-goal">Goal type</label>
              <select id="diet-goal" className="app-select" value={form.goal_type} onChange={(e) => setForm({ ...form, goal_type: e.target.value })}>
                <option value="general">General</option>
                <option value="muscle">Muscle gain</option>
                <option value="lose">Weight loss</option>
              </select>
            </div>

            <div className="app-field">
              <label htmlFor="diet-meal-type">Meal type</label>
              <select id="diet-meal-type" className="app-select" value={form.meal_type} onChange={(e) => setForm({ ...form, meal_type: e.target.value })}>
                <option>Breakfast</option>
                <option>Lunch</option>
                <option>Dinner</option>
              </select>
            </div>

            <div className="app-field">
              <label htmlFor="diet-day">Day (1-7)</label>
              <input id="diet-day" className="app-input" type="number" min={1} max={7} value={form.day} onChange={(e) => setForm({ ...form, day: e.target.value })} />
            </div>

            <div className="app-field">
              <label htmlFor="diet-name">Meal name</label>
              <input id="diet-name" className="app-input" type="text" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="e.g. Grilled Chicken Salad" />
            </div>

            <div className="app-field">
              <label htmlFor="diet-calories">Calories</label>
              <input id="diet-calories" className="app-input" type="number" value={form.calories} onChange={(e) => setForm({ ...form, calories: e.target.value })} />
            </div>

            <div className="app-field">
              <label htmlFor="diet-protein">Protein</label>
              <input id="diet-protein" className="app-input" type="text" value={form.protein} onChange={(e) => setForm({ ...form, protein: e.target.value })} placeholder="e.g. 35g" />
            </div>

            <div className="admin-modal-actions">
              <button type="button" className="app-button-secondary" onClick={closeModal}>Cancel</button>
              <button type="button" className="app-button" onClick={handleSave}>Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdminDiet;
