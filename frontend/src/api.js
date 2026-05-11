const BASE_URL = "http://127.0.0.1:8000/api/";

export const predictSymptoms = async (symptoms) => {
  const response = await fetch(BASE_URL + "predict-symptom/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ symptoms }),
  });

  return response.json();
};
import React from "react";
import Login from "./components/Login";

function App() {
  return <Login />;
}

export default App;