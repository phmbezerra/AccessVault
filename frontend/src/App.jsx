import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [summary, setSummary] = useState(null);
  const [users, setUsers] = useState([]);
  const [systems, setSystems] = useState([]);
  const [accesses, setAccesses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [summaryRes, usersRes, systemsRes, accessesRes] = await Promise.all([
          fetch("http://127.0.0.1:8000/dashboard/summary"),
          fetch("http://127.0.0.1:8000/users/"),
          fetch("http://127.0.0.1:8000/systems/"),
          fetch("http://127.0.0.1:8000/accesses/"),
        ]);

        const summaryData = await summaryRes.json();
        const usersData = await usersRes.json();
        const systemsData = await systemsRes.json();
        const accessesData = await accessesRes.json();

        setSummary(summaryData);
        setUsers(usersData);
        setSystems(systemsData);
        setAccesses(accessesData);
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="container">
        <h1>AccessVault</h1>
        <p>Carregando dados...</p>
      </div>
    );
  }

  return (
    <div className="container">
      <header className="hero">
        <h1>AccessVault</h1>
        <p>Dashboard de gestão de acessos corporativos</p>
      </header>

      <section className="cards">
        <div className="card">
          <h3>Usuários</h3>
          <p>{summary?.total_users ?? 0}</p>
        </div>
        <div className="card">
          <h3>Sistemas</h3>
          <p>{summary?.total_systems ?? 0}</p>
        </div>
        <div className="card">
          <h3>Acessos</h3>
          <p>{summary?.total_accesses ?? 0}</p>
        </div>
        <div className="card">
          <h3>Acessos Ativos</h3>
          <p>{summary?.active_accesses ?? 0}</p>
        </div>
      </section>

      <section className="panel">
        <h2>Usuários</h2>
        {users.length === 0 ? (
          <p>Nenhum usuário encontrado.</p>
        ) : (
          <ul>
            {users.map((user) => (
              <li key={user.id}>
                <strong>{user.name}</strong> — {user.email} — {user.role}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="panel">
        <h2>Sistemas</h2>
        {systems.length === 0 ? (
          <p>Nenhum sistema encontrado.</p>
        ) : (
          <ul>
            {systems.map((system) => (
              <li key={system.id}>
                <strong>{system.name}</strong> — {system.owner_area} — {system.criticality}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="panel">
        <h2>Acessos</h2>
        {accesses.length === 0 ? (
          <p>Nenhum acesso encontrado.</p>
        ) : (
          <ul>
            {accesses.map((access) => (
              <li key={access.id}>
                <strong>{access.user?.name}</strong> → <strong>{access.system?.name}</strong> —{" "}
                {access.access_level} — {access.status}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default App;