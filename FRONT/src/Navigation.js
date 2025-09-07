import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RoleBasedMap from "./pages/RoleBasedMap";
import AdminPage from "./pages/AdminPage";
import Signup from "./pages/Signup";

function Navigation({ role, setRole }) {
  // 🔹 Ajout des props
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage setRole={setRole} />} />{" "}
        {/* 🔹 Passe setRole */}
        <Route path="/dashboard" element={<RoleBasedMap role={role} />} />{" "}
        {/* 🔹 Passe role */}
        <Route path="/login" element={<LoginPage setRole={setRole} />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default Navigation;
