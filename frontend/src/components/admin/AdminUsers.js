import React, { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import "./Admin.css";

const API = "http://127.0.0.1:8000/api";
const headers = () => ({ Authorization: `Bearer ${localStorage.getItem("access")}` });
const PAGE_SIZE = 8;

function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/admin/users/`, { headers: headers() });
      const data = await res.json();
      setUsers(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  useEffect(() => {
    const totalPages = Math.max(1, Math.ceil(users.length / PAGE_SIZE));
    if (page > totalPages) setPage(totalPages);
  }, [users, page]);

  const handleDelete = async (id, username) => {
    if (!window.confirm(`Delete user "${username}"? This cannot be undone.`)) return;
    try {
      await fetch(`${API}/admin/users/${id}/`, {
        method: "DELETE",
        headers: headers(),
      });
      setUsers((prev) => prev.filter((u) => u.id !== id));
    } catch (e) {
      alert("Failed to delete user.");
    }
  };

  const totalPages = Math.max(1, Math.ceil(users.length / PAGE_SIZE));
  const paginatedUsers = users.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <div className="dashboard-container">
      <section className="log-history-card">
        <div className="log-history-header">
          <div>
            <h3>Registered users</h3>
            <p>{users.filter((u) => !u.is_admin).length} regular user accounts in the system.</p>
          </div>
        </div>

        {loading ? (
          <div className="app-empty-state">
            <p>Loading users...</p>
          </div>
        ) : users.length === 0 ? (
          <div className="app-empty-state">
            <p>No users found.</p>
          </div>
        ) : (
          <div className="log-history-table-wrap">
            <table className="log-history-table">
              <thead>
                <tr>
                  <th className="col-id">ID</th>
                  <th>Username / Email</th>
                  <th>Full name</th>
                  <th>Fitness goal</th>
                  <th>Allergies</th>
                  <th className="col-date">Joined</th>
                  <th className="col-role">Role</th>
                  <th className="col-actions">Action</th>
                </tr>
              </thead>
              <tbody>
                {paginatedUsers.map((u) => (
                  <tr key={u.id}>
                    <td className="cell-strong">{u.id}</td>
                    <td className="cell-wrap">{u.username}</td>
                    <td className="cell-wrap">{u.full_name || "--"}</td>
                    <td className="cell-wrap">{u.fitness_goal || "--"}</td>
                    <td className="cell-wrap">{u.allergies || "--"}</td>
                    <td>{u.date_joined}</td>
                    <td className="cell-center">
                      <span className={u.is_admin ? "admin-badge admin-badge-blue" : "admin-badge"}>
                        {u.is_admin ? "Admin" : "User"}
                      </span>
                    </td>
                    <td className="admin-action-cell">
                      {!u.is_admin && (
                        <button type="button" className="app-button-danger admin-inline-btn" onClick={() => handleDelete(u.id, u.username)}>
                          <Trash2 size={14} />
                          Delete
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {!loading && users.length > 0 && (
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
    </div>
  );
}

export default AdminUsers;
