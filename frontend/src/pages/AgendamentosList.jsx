import { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate, useParams } from "react-router-dom";

export default function AgendamentosList() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [agendamentos, setAgendamentos] = useState([]);

  const fetchAgendamentos = async () => {
    const res = await api.get(`/agendamentos/?paciente__id=${id}`);
    setAgendamentos(res.data);
  };

  useEffect(() => {
    fetchAgendamentos();
  }, [id]);

  return (
    <div className="p-8">
      <h1 className="text-3xl mb-4">Agendamentos</h1>
      <button
        onClick={() => navigate(`/pacientes/${id}/agendamentos/novo`)}
        className="btn btn-primary mb-4"
      >
        + Novo Agendamento
      </button>

      <div className="overflow-x-auto">
        <table className="table table-zebra">
          <thead>
            <tr>
              <th>Data</th>
              <th>Hora</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {agendamentos.map((a) => (
              <tr key={a.id}>
                <td>{a.data}</td>
                <td>{a.hora}</td>
                <td>{a.status}</td>
                <td className="space-x-2">
                  <button
                    onClick={() => navigate(`/agendamentos/${a.id}/editar`)}
                    className="btn btn-sm btn-info"
                  >
                    Editar
                  </button>
                  {a.status === "EM_ANDAMENTO" && (
                    <button
                      onClick={() => navigate(`/consulta/${a.id}`)}
                      className="btn btn-sm btn-secondary"
                    >
                      Consulta
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
