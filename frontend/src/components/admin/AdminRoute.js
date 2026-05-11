import React from "react";
import { Navigate } from "react-router-dom";
import { getIsAdmin } from "../../utils/auth";

function AdminRoute({ children }) {
  const token = localStorage.getItem("access");

  if (!token || !getIsAdmin()) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default AdminRoute;
