import { useForm } from "react-hook-form";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Login() {
  const { register, handleSubmit } = useForm();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const onSubmit = async (data) => {
    try {
      setError("");
      await login(data.username, data.password);
      navigate("/dashboard");
    } catch (err) {
      setError("Usuário ou senha inválidos.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-base-200">
      <div className="card w-96 bg-base-100 shadow-xl">
        <div className="card-body">
          <h2 className="card-title justify-center mb-4">Login</h2>

          {error && (
            <div className="alert alert-error p-2 mb-4">
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-3">
            <input
              {...register("username")}
              type="text"
              placeholder="Usuário"
              className="input input-bordered w-full"
              required
            />

            <input
              {...register("password")}
              type="password"
              placeholder="Senha"
              className="input input-bordered w-full"
              required
            />

            <div className="card-actions mt-2">
              <button className="btn btn-primary w-full">Entrar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
