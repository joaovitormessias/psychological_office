import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect } from "react";
import api from "../services/api";

export default function PacienteForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { register, handleSubmit, setValue } = useForm();

  const isEdit = !!id;

  const onSubmit = async (data) => {
    // TODO: Enhance error handling for API requests (e.g., try-catch, display messages).
    // TODO: The backend PacienteSerializer expects nested objects for 'endereco_residencial'
    // and 'endereco_cobranca'. Currently, this form submits a flat data structure.
    // This will likely cause issues. The data structure should be:
    // {
    //   ...pacienteFields,
    //   endereco_residencial: { cep, uf, cidade, logradouro, numero, bairro },
    //   endereco_cobranca: { cep, uf, cidade, logradouro, numero, bairro }, // or null
    //   repetir_endereco_cobranca: boolean
    // }
    if (isEdit) {
      await api.patch(`/pacientes/${id}/`, data);
    } else {
      await api.post("/pacientes/", data);
    }
    navigate("/pacientes");
  };

  const fetchData = async () => {
    const res = await api.get(`/pacientes/${id}/`);
    const paciente = res.data;
    Object.keys(paciente).forEach((key) => {
      if (paciente[key] != null) {
        setValue(key, paciente[key]);
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
      <h1 className="text-3xl mb-4">{isEdit ? "Editar" : "Novo"} Paciente</h1>
      {/* TODO: This form is missing fields for address details:
          - endereco_residencial (cep, uf, cidade, logradouro, numero, bairro) - Required
          - endereco_cobranca (cep, uf, cidade, logradouro, numero, bairro) - Optional
          - A checkbox or similar for 'repetir_endereco_cobranca'
          These fields need to be added and structured correctly for the API.
      */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <input {...register("nome")} placeholder="Nome" className="input input-bordered w-full" required />
        <input {...register("cpf")} placeholder="CPF" className="input input-bordered w-full" required disabled={isEdit} />
        <input {...register("nascimento")} placeholder="Data de Nascimento" type="date" className="input input-bordered w-full" required />
        <input {...register("celular")} placeholder="Celular" className="input input-bordered w-full" required />
        <input {...register("whatsapp")} placeholder="WhatsApp" className="input input-bordered w-full" />
        <input {...register("email")} placeholder="Email" className="input input-bordered w-full" required />
        <button className="btn btn-primary w-full">Salvar</button>
      </form>
    </div>
  );
}
