import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services/api";

export default function Consulta() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue } = useForm();
  const [dados, setDados] = useState({});

  const onSubmit = async (data) => {
    await api.post("/consultas/", {
      agendamento_id: id,
      ...data,
      concluir_consulta: true,
    });
    navigate("/dashboard");
  };

  const fetchData = async () => {
    const res = await api.get(`/agendamentos/${id}/`);
    setDados(res.data);
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  return (
    <div className="p-8">
      <h1 className="text-3xl mb-4">Consulta</h1>
      <div className="mb-4">
        <p><b>Paciente:</b> {dados?.paciente_nome}</p>
        <p><b>Data:</b> {dados?.data}</p>
        <p><b>Hora:</b> {dados?.hora}</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <textarea {...register("anotacoes_atuais")} placeholder="Anotações da Consulta" className="textarea textarea-bordered w-full" required />
        <textarea {...register("pontos_atencao")} placeholder="Pontos de Atenção" className="textarea textarea-bordered w-full" />
        <button className="btn btn-primary w-full">Salvar e Concluir</button>
      </form>
    </div>
  );
}
