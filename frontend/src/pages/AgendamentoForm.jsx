import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect } from "react";
import api from "../services/api";

export default function AgendamentoForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue } = useForm();

  const isEdit = window.location.pathname.includes("/editar");

  const onSubmit = async (data) => {
    if (isEdit) {
      await api.patch(`/agendamentos/${id}/`, data);
    } else {
      await api.post("/agendamentos/", { ...data, paciente_id: id });
    }
    navigate(`/pacientes/${id}/agendamentos`);
  };

  const fetchData = async () => {
    const res = await api.get(`/agendamentos/${id}/`);
    const agendamento = res.data;
    Object.keys(agendamento).forEach((key) => {
      if (agendamento[key] != null) {
        setValue(key, agendamento[key]);
      }
    });
  };

  useEffect(() => {
    if (isEdit) {
      fetchData();
    }
  }, [id]);

  return (
    <div className="p-8">
      <h1 className="text-3xl mb-4">{isEdit ? "Editar" : "Novo"} Agendamento</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <input {...register("data")} type="date" className="input input-bordered w-full" required />
        <input {...register("hora")} type="time" className="input input-bordered w-full" required />
        <textarea {...register("observacoes")} placeholder="Observações" className="textarea textarea-bordered w-full" />
        <button className="btn btn-primary w-full">Salvar</button>
      </form>
    </div>
  );
}
