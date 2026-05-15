import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [activeSection, setActiveSection] = useState("dashboard");

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

  const [userForm, setUserForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "colaborador",
  });

  const [userFormLoading, setUserFormLoading] = useState(false);
  const [userFormMessage, setUserFormMessage] = useState("");
  const [userFormError, setUserFormError] = useState("");

  const [systemForm, setSystemForm] = useState({
    name: "",
    description: "",
    owner_area: "",
    criticality: "media",
  });

  const [systemFormLoading, setSystemFormLoading] = useState(false);
  const [systemFormMessage, setSystemFormMessage] = useState("");
  const [systemFormError, setSystemFormError] = useState("");

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

  const handleUserFormChange = (event) => {
    const { name, value } = event.target;
    setUserForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSystemFormChange = (event) => {
    const { name, value } = event.target;
    setSystemForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCreateUser = async (event) => {
    event.preventDefault();

    try {
      setUserFormLoading(true);
      setUserFormMessage("");
      setUserFormError("");

      const response = await fetch(`${API_BASE}/users/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userForm),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const apiMessage =
          errorData?.detail || "Não foi possível cadastrar o usuário.";

        throw new Error(
          typeof apiMessage === "string"
            ? apiMessage
            : "Não foi possível cadastrar o usuário."
        );
      }

      setUserForm({
        name: "",
        email: "",
        password: "",
        role: "colaborador",
      });

      setUserFormMessage("Usuário cadastrado com sucesso.");
      await fetchAllData();
    } catch (err) {
      setUserFormError(err.message || "Erro ao cadastrar usuário.");
    } finally {
      setUserFormLoading(false);
    }
  };

  const handleCreateSystem = async (event) => {
    event.preventDefault();

    try {
      setSystemFormLoading(true);
      setSystemFormMessage("");
      setSystemFormError("");

      const response = await fetch(`${API_BASE}/systems/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(systemForm),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const apiMessage =
          errorData?.detail || "Não foi possível cadastrar o sistema.";

        throw new Error(
          typeof apiMessage === "string"
            ? apiMessage
            : "Não foi possível cadastrar o sistema."
        );
      }

      setSystemForm({
        name: "",
        description: "",
        owner_area: "",
        criticality: "media",
      });

      setSystemFormMessage("Sistema cadastrado com sucesso.");
      await fetchAllData();
    } catch (err) {
      setSystemFormError(err.message || "Erro ao cadastrar sistema.");
    } finally {
      setSystemFormLoading(false);
    }
  };

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

  const renderDashboard = () => (
    <>
      <section className="hero-card">
        <div className="hero-card-left">
          <h2>Visão geral do ambiente</h2>
          <p>
            Acompanhe usuários, sistemas e permissões de acesso em um único painel.
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
    </>
  );

  const renderUsers = () => (
    <>
      <section className="form-section">
        <div className="section-heading">
          <h2>Cadastrar usuário</h2>
          <span>Criação direta pela interface</span>
        </div>

        <form className="form-card" onSubmit={handleCreateUser}>
          <div className="form-grid">
            <div className="form-field">
              <label htmlFor="name">Nome</label>
              <input
                id="name"
                name="name"
                type="text"
                value={userForm.name}
                onChange={handleUserFormChange}
                placeholder="Digite o nome"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={userForm.email}
                onChange={handleUserFormChange}
                placeholder="Digite o email"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="password">Senha</label>
              <input
                id="password"
                name="password"
                type="password"
                value={userForm.password}
                onChange={handleUserFormChange}
                placeholder="Mínimo de 6 caracteres"
                minLength={6}
                maxLength={72}
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="role">Perfil</label>
              <select
                id="role"
                name="role"
                value={userForm.role}
                onChange={handleUserFormChange}
              >
                <option value="colaborador">colaborador</option>
                <option value="gestor">gestor</option>
                <option value="admin">admin</option>
              </select>
            </div>
          </div>

          <div className="form-actions">
            <button
              className="primary-button"
              type="submit"
              disabled={userFormLoading}
            >
              {userFormLoading ? "Cadastrando..." : "Cadastrar usuário"}
            </button>
          </div>

          {userFormMessage && (
            <p className="form-message success">{userFormMessage}</p>
          )}

          {userFormError && (
            <p className="form-message error">{userFormError}</p>
          )}
        </form>
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
    </>
  );

  const renderSystems = () => (
    <>
      <section className="form-section">
        <div className="section-heading">
          <h2>Cadastrar sistema</h2>
          <span>Gestão de sistemas corporativos</span>
        </div>

        <form className="form-card" onSubmit={handleCreateSystem}>
          <div className="form-grid">
            <div className="form-field">
              <label htmlFor="system-name">Nome do sistema</label>
              <input
                id="system-name"
                name="name"
                type="text"
                value={systemForm.name}
                onChange={handleSystemFormChange}
                placeholder="Ex.: Portal RH"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="owner_area">Área responsável</label>
              <input
                id="owner_area"
                name="owner_area"
                type="text"
                value={systemForm.owner_area}
                onChange={handleSystemFormChange}
                placeholder="Ex.: Recursos Humanos"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="description">Descrição</label>
              <input
                id="description"
                name="description"
                type="text"
                value={systemForm.description}
                onChange={handleSystemFormChange}
                placeholder="Descreva brevemente o sistema"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="criticality">Criticidade</label>
              <select
                id="criticality"
                name="criticality"
                value={systemForm.criticality}
                onChange={handleSystemFormChange}
              >
                <option value="baixa">baixa</option>
                <option value="media">media</option>
                <option value="alta">alta</option>
                <option value="critica">critica</option>
              </select>
            </div>
          </div>

          <div className="form-actions">
            <button
              className="primary-button"
              type="submit"
              disabled={systemFormLoading}
            >
              {systemFormLoading ? "Cadastrando..." : "Cadastrar sistema"}
            </button>
          </div>

          {systemFormMessage && (
            <p className="form-message success">{systemFormMessage}</p>
          )}

          {systemFormError && (
            <p className="form-message error">{systemFormError}</p>
          )}
        </form>
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
    </>
  );

  const renderAccesses = () => (
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
  );

  return (
    <div className="app shell">
      <div className="background-glow background-glow-1" />
      <div className="background-glow background-glow-2" />

      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="badge">Access Management</span>
          <h1>AccessVault</h1>
          <p>Painel corporativo</p>
        </div>

        <nav className="sidebar-nav">
          <button
            className={activeSection === "dashboard" ? "nav-item active" : "nav-item"}
            onClick={() => setActiveSection("dashboard")}
          >
            <span>📊</span>
            Dashboard
          </button>

          <button
            className={activeSection === "users" ? "nav-item active" : "nav-item"}
            onClick={() => setActiveSection("users")}
          >
            <span>👤</span>
            Usuários
          </button>

          <button
            className={activeSection === "systems" ? "nav-item active" : "nav-item"}
            onClick={() => setActiveSection("systems")}
          >
            <span>🖥️</span>
            Sistemas
          </button>

          <button
            className={activeSection === "accesses" ? "nav-item active" : "nav-item"}
            onClick={() => setActiveSection("accesses")}
          >
            <span>🔐</span>
            Acessos
          </button>
        </nav>

        <div className="sidebar-footer">
          <a
            className="ghost-button sidebar-link"
            href={`${API_BASE}/docs`}
            target="_blank"
            rel="noreferrer"
          >
            Ver API
          </a>
          <button className="primary-button sidebar-link" onClick={fetchAllData}>
            Atualizar dados
          </button>
        </div>
      </aside>

      <div className="main-content">
        <header className="topbar topbar-main">
          <div>
            <p className="page-label">
              {activeSection === "dashboard" && "Dashboard geral"}
              {activeSection === "users" && "Gestão de usuários"}
              {activeSection === "systems" && "Gestão de sistemas"}
              {activeSection === "accesses" && "Gestão de acessos"}
            </p>
            <h2 className="page-title">
              {activeSection === "dashboard" && "Visão geral do ambiente"}
              {activeSection === "users" && "Usuários"}
              {activeSection === "systems" && "Sistemas"}
              {activeSection === "accesses" && "Acessos"}
            </h2>
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
        </header>

        {error && (
          <section className="alert-card">
            <strong>Erro:</strong> {error}
          </section>
        )}

        <main className="dashboard">
          {activeSection === "dashboard" && renderDashboard()}
          {activeSection === "users" && renderUsers()}
          {activeSection === "systems" && renderSystems()}
          {activeSection === "accesses" && renderAccesses()}
        </main>
      </div>
    </div>
  );
}

export default App;