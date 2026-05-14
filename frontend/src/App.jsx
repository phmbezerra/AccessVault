import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState({
    total_users: 0,
    active_users: 0,
    inactive_users: 0,
    total_systems: 0,
    active_systems: 0,
    inactive_systems: 0,
    total_accesses: 0,
    active_accesses: 0,
    revoked_accesses: 0,
    pending_accesses: 0,
  });

  const [users, setUsers] = useState([]);
  const [systems, setSystems] = useState([]);
  const [accesses, setAccesses] = useState([]);

  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState("");
  const [error, setError] = useState("");

  const fetchAllData = async () => {
    try {
      setLoading(true);
      setError("");

      const [summaryRes, usersRes, systemsRes, accessesRes] = await Promise.all([
        fetch(`${API_BASE}/dashboard/summary`),
        fetch(`${API_BASE}/users/`),
        fetch(`${API_BASE}/systems/`),
        fetch(`${API_BASE}/accesses/`),
      ]);

      if (!summaryRes.ok || !usersRes.ok || !systemsRes.ok || !accessesRes.ok) {
        throw new Error("Falha ao carregar os dados da aplicação.");
      }

      const [summaryData, usersData, systemsData, accessesData] =
        await Promise.all([
          summaryRes.json(),
          usersRes.json(),
          systemsRes.json(),
          accessesRes.json(),
        ]);

      setSummary(summaryData);
      setUsers(usersData);
      setSystems(systemsData);
      setAccesses(accessesData);
      setLastUpdate(new Date().toLocaleString("pt-BR"));
    } catch (err) {
      setError(err.message || "Erro inesperado ao carregar a dashboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  const mainCards = [
    {
      title: "Usuários",
      value: summary.total_users,
      icon: "👤",
      description: `${summary.active_users} ativos • ${summary.inactive_users} inativos`,
    },
    {
      title: "Sistemas",
      value: summary.total_systems,
      icon: "🖥️",
      description: `${summary.active_systems} ativos • ${summary.inactive_systems} inativos`,
    },
    {
      title: "Acessos",
      value: summary.total_accesses,
      icon: "🔐",
      description: `${summary.active_accesses} ativos no total`,
    },
    {
      title: "Acessos Ativos",
      value: summary.active_accesses,
      icon: "✅",
      description: "Permissões atualmente válidas",
    },
  ];

  const statusCards = [
    {
      label: "Acessos pendentes",
      value: summary.pending_accesses,
      tone: "warning",
    },
    {
      label: "Acessos revogados",
      value: summary.revoked_accesses,
      tone: "danger",
    },
    {
      label: "Usuários inativos",
      value: summary.inactive_users,
      tone: "neutral",
    },
    {
      label: "Sistemas inativos",
      value: summary.inactive_systems,
      tone: "neutral",
    },
  ];

  return (
    <div className="app">
      <div className="background-glow background-glow-1" />
      <div className="background-glow background-glow-2" />

      <header className="topbar">
        <div>
          <span className="badge">Access Management</span>
          <h1>AccessVault</h1>
          <p>Dashboard de gestão de acessos corporativos</p>
        </div>

        <div className="topbar-actions">
          <a
            className="ghost-button"
            href={`${API_BASE}/docs`}
            target="_blank"
            rel="noreferrer"
          >
            Ver API
          </a>

          <button className="primary-button" onClick={fetchAllData}>
            Atualizar dashboard
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="hero-card">
          <div className="hero-card-left">
            <h2>Visão geral do ambiente</h2>
            <p>
              Acompanhe usuários, sistemas e permissões de acesso em um único
              painel.
            </p>
          </div>

          <div className="hero-card-right">
            <div className={`status-pill ${error ? "offline" : "online"}`}>
              <span className="status-dot" />
              {error ? "API com problema" : "API online"}
            </div>
            <span className="last-update">
              {lastUpdate ? `Última atualização: ${lastUpdate}` : "Carregando..."}
            </span>
          </div>
        </section>

        {error && (
          <section className="alert-card">
            <strong>Erro:</strong> {error}
          </section>
        )}

        <section className="cards-grid">
          {mainCards.map((card) => (
            <article className="stat-card" key={card.title}>
              <div className="stat-card-top">
                <span className="stat-icon">{card.icon}</span>
                <span className="stat-title">{card.title}</span>
              </div>

              <div className="stat-value">{loading ? "..." : card.value}</div>
              <p className="stat-description">{card.description}</p>
            </article>
          ))}
        </section>

        <section className="bottom-grid">
          <article className="panel">
            <div className="panel-header">
              <h3>Status rápidos</h3>
              <span className="panel-tag">Resumo operacional</span>
            </div>

            <div className="mini-stats">
              {statusCards.map((item) => (
                <div className={`mini-stat ${item.tone}`} key={item.label}>
                  <span>{item.label}</span>
                  <strong>{loading ? "..." : item.value}</strong>
                </div>
              ))}
            </div>
          </article>

          <article className="panel">
            <div className="panel-header">
              <h3>Ações rápidas</h3>
              <span className="panel-tag">Atalhos úteis</span>
            </div>

            <div className="quick-actions">
              <a href={`${API_BASE}/docs`} target="_blank" rel="noreferrer">
                Abrir Swagger
              </a>
              <a href={`${API_BASE}/users/`} target="_blank" rel="noreferrer">
                Ver usuários
              </a>
              <a href={`${API_BASE}/systems/`} target="_blank" rel="noreferrer">
                Ver sistemas
              </a>
              <a href={`${API_BASE}/accesses/`} target="_blank" rel="noreferrer">
                Ver acessos
              </a>
            </div>
          </article>
        </section>

        <section className="table-section">
          <div className="section-heading">
            <h2>Usuários cadastrados</h2>
            <span>{users.length} registros</span>
          </div>

          <div className="table-card">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Email</th>
                  <th>Perfil</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {users.length > 0 ? (
                  users.map((user) => (
                    <tr key={user.id}>
                      <td>{user.name}</td>
                      <td>{user.email}</td>
                      <td>
                        <span className="role-badge">{user.role}</span>
                      </td>
                      <td>
                        <span
                          className={`status-badge ${
                            user.is_active ? "active" : "inactive"
                          }`}
                        >
                          {user.is_active ? "Ativo" : "Inativo"}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="empty-cell">
                      Nenhum usuário encontrado.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        <section className="table-section">
          <div className="section-heading">
            <h2>Sistemas cadastrados</h2>
            <span>{systems.length} registros</span>
          </div>

          <div className="table-card">
            <table>
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Área responsável</th>
                  <th>Criticidade</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {systems.length > 0 ? (
                  systems.map((system) => (
                    <tr key={system.id}>
                      <td>{system.name}</td>
                      <td>{system.owner_area}</td>
                      <td>
                        <span className="role-badge">{system.criticality}</span>
                      </td>
                      <td>
                        <span
                          className={`status-badge ${
                            system.is_active ? "active" : "inactive"
                          }`}
                        >
                          {system.is_active ? "Ativo" : "Inativo"}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="empty-cell">
                      Nenhum sistema encontrado.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        <section className="table-section">
          <div className="section-heading">
            <h2>Acessos cadastrados</h2>
            <span>{accesses.length} registros</span>
          </div>

          <div className="table-card">
            <table>
              <thead>
                <tr>
                  <th>Usuário</th>
                  <th>Sistema</th>
                  <th>Nível</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {accesses.length > 0 ? (
                  accesses.map((access) => (
                    <tr key={access.id}>
                      <td>{access.user?.name || `Usuário #${access.user_id}`}</td>
                      <td>{access.system?.name || `Sistema #${access.system_id}`}</td>
                      <td>
                        <span className="role-badge">{access.access_level}</span>
                      </td>
                      <td>
                        <span
                          className={`status-badge ${
                            access.is_active ? "active" : "inactive"
                          }`}
                        >
                          {access.status}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="empty-cell">
                      Nenhum acesso encontrado.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;