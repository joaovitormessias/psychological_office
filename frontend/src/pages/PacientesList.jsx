import { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

export default function PacientesList() {
  const [pacientes, setPacientes] = useState([]);
  const navigate = useNavigate();

  const fetchPacientes = async () => {
    const res = await api.get("/pacientes/");
    setPacientes(res.data);
  };

  useEffect(() => {
    fetchPacientes();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Lista de Pacientes</h1>
      <button
        onClick={() => navigate("/pacientes/novo")}
        className="btn btn-primary mb-4"
      >
        + Novo Paciente
      </button>

      <div className="overflow-x-auto">
        <table className="table table-zebra">
          <thead>
            <tr>
              <th>Nome</th>
              <th>CPF</th>
              <th>WhatsApp</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {pacientes.map((p) => (
              <tr key={p.id}>
                <td>{p.nome}</td>
                <td>{p.cpf}</td>
                <td>
                  {p.whatsapp_link ? (
                    <a href={p.whatsapp_link} target="_blank" className="link">
                      WhatsApp
                    </a>
                  ) : (
                    "-"
                  )}
                </td>
                <td className="space-x-2">
                  <button
                    onClick={() => navigate(`/pacientes/${p.id}`)}
                    className="btn btn-sm btn-info"
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => navigate(`/pacientes/${p.id}/agendamentos`)}
                    className="btn btn-sm btn-secondary"
                  >
                    Agendamentos
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
