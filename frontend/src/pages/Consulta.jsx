import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services/api";

export default function Consulta() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue } = useForm();
  const [dados, setDados] = useState({}); // Stores agendamento details for display
  // const [anotacoesAnteriores, setAnotacoesAnteriores] = useState(""); // Optional: For displaying previous notes

  const onSubmit = async (data) => {
    // TODO: Implement .catch() for API calls to handle errors from the backend.
    // For example, the backend might return errors if:
    // - The agendamento_id is invalid or already has a consultation.
    // - The agendamento is not in 'EM_ANDAMENTO' status.
    // - The user is not a 'PROFISSIONAL_SAUDE'.
    // These errors should be displayed to the user.
    try {
      await api.post("/consultas/", {
        agendamento_id: id, // 'id' from useParams() is the agendamento_id
        ...data, // Contains anotacoes_atuais, pontos_atencao
        concluir_consulta: true, // Always concludes the appointment upon saving this consultation
      });
      navigate("/dashboard");
    } catch (error) {
      console.error("Erro ao salvar consulta:", error);
      // Add user-facing error message display here, e.g., using a toast notification or state variable.
      // if (error.response && error.response.data && error.response.data.detail) {
      //   alert(`Erro: ${error.response.data.detail}`);
      // } else if (error.response && error.response.data) {
      //   alert(`Erro: ${JSON.stringify(error.response.data)}`);
      // } else {
      //   alert("Ocorreu um erro ao salvar a consulta.");
      // }
    }
  };

  const fetchData = async () => {
    // This fetches Agendamento details for context (patient name, date, time).
    // The backend's ConsultaSerializer will automatically populate 'anotacoes_anteriores'
    // when the new Consulta is created. If these notes need to be displayed *before* submission,
    // a separate mechanism or endpoint would be needed to fetch them based on the agendamento_id.
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
        {/* If anotacoesAnteriores state were used and populated:
        {anotacoesAnteriores && (
          <div className="mt-2 p-2 border rounded bg-gray-100">
            <h3 className="font-semibold">Anotações Anteriores:</h3>
            <p className="whitespace-pre-wrap">{anotacoesAnteriores}</p>
          </div>
        )}
        */}
      </div>

      {/* This form supports fields currently in the backend: 'anotacoes_atuais', 'pontos_atencao'.
          Fields like 'queixa_principal', 'exame_fisico', 'diagnostico', 'prescricao' are
          not part of the current backend Consulta model/serializer. If they are required,
          the backend needs to be updated first.
      */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <textarea {...register("anotacoes_atuais")} placeholder="Anotações da Consulta" className="textarea textarea-bordered w-full" required />
        <textarea {...register("pontos_atencao")} placeholder="Pontos de Atenção" className="textarea textarea-bordered w-full" />
        <button className="btn btn-primary w-full">Salvar e Concluir</button>
      </form>
    </div>
  );
}
