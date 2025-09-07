import React from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import UserTable from "../components/UserTable";
import FileManagement from "../components/FileManagement";
import "../styles/admin.css";

function AdminPage() {
  return (
    <div className="container">
      <Header />
      <h2 className="admin-page-title">Page d'Administration</h2>

      <UserTable />
      <FileManagement />

      <Footer />
    </div>
  );
}

export default AdminPage;
