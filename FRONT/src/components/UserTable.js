import React, { useState, useEffect } from "react";
import axios from "axios";
import apiRoutes from "../apiroutes.js";

const UserTable = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [newUser, setNewUser] = useState({
    login: "",
    password: "",
    role: 1,
  });

  async function fetchUsers() {
    try {
      const response = await axios.get(apiRoutes.getUsers, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });

      const roleNames = {
        0: "Admin",
        1: "Capitaine",
        2: "Armateur",
        3: "Expert",
      };

      const sortedUsers = response.data
        .map((user) => ({
          ...user,
          roleName: roleNames[user.IDRole],
        }))
        .sort((a, b) => a.IDUser - b.IDUser);

      setUsers(sortedUsers);
    } catch (err) {
      setError("Impossible de récupérer les utilisateurs.");
    }
  }

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleAddUser = async () => {
    if (!newUser.login || !newUser.password) {
      setError("Le nom et le mot de passe sont requis.");
      return;
    }

    try {
      await axios.post(
        apiRoutes.addUser,
        {
          Login: newUser.login,
          Password: newUser.password,
          IDRole: parseInt(newUser.role),
        },
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );

      fetchUsers();
      setNewUser({ login: "", password: "", role: 1 });
      setError("");
    } catch (err) {
      setError("Erreur lors de l'ajout de l'utilisateur.");
    }
  };

  const handleEditUser = async (userId, updatedFields) => {
    const userToUpdate = users.find((user) => user.IDUser === userId);

    const updatedUser = {
      Login: updatedFields.login ?? userToUpdate.Login,
      Password: updatedFields.password ?? null,
      IDRole:
        updatedFields.role !== undefined
          ? parseInt(updatedFields.role)
          : userToUpdate.IDRole,
    };

    console.log("Données envoyées à l'API:", updatedUser);

    try {
      await axios.put(apiRoutes.editUser(userId), updatedUser, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });

      setUsers(
        users.map((user) =>
          user.IDUser === userId ? { ...user, ...updatedUser } : user
        )
      );
    } catch (err) {
      console.error("Erreur API:", err.response?.data);
      setError("Erreur lors de la modification de l'utilisateur.");
    }
  };

  const handleDeleteUser = async (userId) => {
    try {
      await axios.delete(apiRoutes.deleteUser(userId), {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      setUsers(users.filter((user) => user.IDUser !== userId));
    } catch (err) {
      setError("Erreur lors de la suppression de l'utilisateur.");
    }
  };

  return (
    <div className="admin-table-container">
      {error && <p className="admin-error">{error}</p>}

      <div className="admin-add-user">
        <input
          type="text"
          placeholder="Nom de l'utilisateur"
          value={newUser.login}
          onChange={(e) => setNewUser({ ...newUser, login: e.target.value })}
        />
        <input
          type="password"
          placeholder="Mot de passe"
          value={newUser.password}
          onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
        />
        <select
          value={newUser.role}
          onChange={(e) =>
            setNewUser({ ...newUser, role: parseInt(e.target.value) })
          }
        >
          <option value={1}>Capitaine</option>
          <option value={2}>Armateur</option>
          <option value={3}>Expert</option>
          <option value={0}>Admin</option>
        </select>
        <button onClick={handleAddUser}>Ajouter</button>
      </div>

      <table className="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nom</th>
            <th>Rôle</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.IDUser}>
              <td>{user.IDUser}</td>
              <td>
                <input
                  type="text"
                  value={user.Login}
                  onChange={(e) =>
                    handleEditUser(user.IDUser, { login: e.target.value })
                  }
                />
              </td>
              <td>
                <select
                  value={user.IDRole}
                  onChange={(e) =>
                    handleEditUser(user.IDUser, {
                      role: parseInt(e.target.value),
                    })
                  }
                >
                  <option value={1}>Capitaine</option>
                  <option value={2}>Armateur</option>
                  <option value={3}>Expert</option>
                  <option value={0}>Admin</option>
                </select>
              </td>
              <td>
                <button onClick={() => handleDeleteUser(user.IDUser)}>
                  Supprimer
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserTable;
