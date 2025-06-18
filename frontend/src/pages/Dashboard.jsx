import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleNavigate = (path) => navigate(path);

  return (
    <div className="p-8 space-y-4">
      <h1 className="text-3xl font-bold">Bem-vindo, {user?.username}</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Pacientes</h2>
            <p>Gerencie os pacientes do consultório.</p>
            <div className="card-actions justify-end">
              <button onClick={() => handleNavigate("/pacientes")} className="btn btn-primary">
                Acessar
              </button>
            </div>
          </div>
        </div>

        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Agendamentos</h2>
            <p>Visualize e gerencie os agendamentos.</p>
            <div className="card-actions justify-end">
              <button onClick={() => handleNavigate("/pacientes")} className="btn btn-primary">
                Acessar
              </button>
            </div>
          </div>
        </div>

        {user?.role === "PROFISSIONAL_SAUDE" && (
          <div className="card bg-base-100 shadow-xl">
            <div className="card-body">
              <h2 className="card-title">Consultas</h2>
              <p>Inicie e registre suas consultas.</p>
              <div className="card-actions justify-end">
                <button className="btn btn-primary">Acessar</button>
              </div>
            </div>
          </div>
        )}
      </div>

      <button onClick={logout} className="btn btn-error">
        Sair
      </button>
    </div>
  );
}
