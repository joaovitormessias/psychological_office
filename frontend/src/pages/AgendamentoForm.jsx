import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect } from "react";
import api from "../services/api";

export default function AgendamentoForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue } = useForm();
  // Store pacienteId for redirect logic, especially after editing.
  const [pacienteIdForRedirect, setPacienteIdForRedirect] = React.useState(null);


  // TODO: Consider a more robust way to determine edit mode, e.g., based on route parameters
  // (e.g., if an agendamentoId route param exists specifically for editing an agendamento).
  // Current logic assumes '/editar' in path means editing an agendamento, and 'id' is agendamentoId.
  // For new agendamentos (e.g. /pacientes/:pacienteId/agendamentos/novo), 'id' is pacienteId.
  const isEdit = window.location.pathname.includes("/editar");

  const onSubmit = async (data) => {
    // TODO: Implement .catch() for API calls to handle errors, especially validation errors
    // from the backend (e.g., double booking, time out of range).
    // Display user-friendly messages based on error responses.
    try {
      if (isEdit) {
        // 'id' from useParams() is agendamento_id in edit mode
        await api.patch(`/agendamentos/${id}/`, data);
        // Use the stored pacienteIdForRedirect for navigation
        if (pacienteIdForRedirect) {
          navigate(`/pacientes/${pacienteIdForRedirect}/agendamentos`);
        } else {
          // Fallback or error if pacienteIdForRedirect is not set
          navigate("/pacientes"); // Or a more appropriate fallback
        }
      } else {
        // 'id' from useParams() is paciente_id in new mode
        await api.post("/agendamentos/", { ...data, paciente_id: id });
        navigate(`/pacientes/${id}/agendamentos`);
      }
    } catch (error) {
      console.error("Failed to save agendamento:", error);
      // Add user-facing error message display here
    }
  };

  const fetchData = async () => {
    // 'id' from useParams() is agendamento_id in edit mode
    const res = await api.get(`/agendamentos/${id}/`);
    const agendamento = res.data;
    Object.keys(agendamento).forEach((key) => {
      if (agendamento[key] != null) {
        // The backend sends 'data' (date) and 'hora' which are directly usable by the inputs.
        setValue(key, agendamento[key]);
      }
    });
    // Store paciente_id from the fetched agendamento for correct redirection after editing.
    // The backend serializer provides 'paciente_id' as a write_only field but it's part of the Agendamento model.
    // Assuming the GET request to /agendamentos/:id/ returns the patient's ID, e.g. as 'paciente' or 'paciente_id'.
    // If it's nested like agendamento.paciente.id, adjust accordingly.
    // For now, assuming 'paciente_id' is directly available or it is 'paciente' (if it's an ID string/number).
    // Let's assume the serializer sends 'paciente' as the ID of the patient.
    if (agendamento.paciente) { // Or agendamento.paciente_id if that's what the API sends
      setPacienteIdForRedirect(agendamento.paciente);
    } else if (agendamento.paciente_id) { // Check common variations
        setPacienteIdForRedirect(agendamento.paciente_id)
    }
    // If patient ID is nested, e.g. agendamento.paciente.id:
    // else if (agendamento.paciente && agendamento.paciente.id) {
    //   setPacienteIdForRedirect(agendamento.paciente.id);
    // }
  };

  useEffect(() => {
    if (isEdit) {
      // In edit mode, 'id' is agendamento_id
      fetchData();
    } else {
      // In new mode, 'id' (from /pacientes/:id/agendamentos/novo) is patient_id
      setPacienteIdForRedirect(id); // Set for consistency, though not strictly needed for new's redirect
    }
  }, [id, isEdit]);

  return (
    <div className="p-8">
      <h1 className="text-3xl mb-4">{isEdit ? "Editar" : "Novo"} Agendamento</h1>
      {/* TODO: The backend AgendamentoSerializer supports updating the patient's residential address
          (fields like 'endereco_residencial_cep', 'endereco_residencial_logradouro', etc.).
          This form currently does not include fields for updating the address.
          If this functionality is desired, relevant input fields should be added.
      */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <input {...register("data")} type="date" className="input input-bordered w-full" required />
        <input {...register("hora")} type="time" className="input input-bordered w-full" required />
        <textarea {...register("observacoes")} placeholder="Observações" className="textarea textarea-bordered w-full" />
        <button className="btn btn-primary w-full">Salvar</button>
      </form>
    </div>
  );
}
