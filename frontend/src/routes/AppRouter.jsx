import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "../contexts/AuthContext";
import PrivateRoute from "./PrivateRoute";

import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import PacientesList from "../pages/PacientesList";
import PacienteForm from "../pages/PacienteForm";
import AgendamentosList from "../pages/AgendamentosList";
import AgendamentoForm from "../pages/AgendamentoForm";
import Consulta from "../pages/Consulta";

export default function AppRouter() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />

          <Route
            path="/dashboard"
            element={
              <PrivateRoute roles={["SECRETARIA", "PROFISSIONAL_SAUDE"]}>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/pacientes"
            element={
              <PrivateRoute roles={["SECRETARIA", "PROFISSIONAL_SAUDE"]}>
                <PacientesList />
              </PrivateRoute>
            }
          />
          <Route
            path="/pacientes/novo"
            element={
              <PrivateRoute roles={["SECRETARIA", "PROFISSIONAL_SAUDE"]}>
                <PacienteForm />
              </PrivateRoute>
            }
          />
          <Route
            path="/pacientes/:id"
            element={
              <PrivateRoute roles={["SECRETARIA", "PROFISSIONAL_SAUDE"]}>
                <PacienteForm />
              </PrivateRoute>
            }
          />
          <Route
            path="/pacientes/:id/agendamentos"
            element={
              <PrivateRoute roles={["SECRETARIA", "PROFISSIONAL_SAUDE"]}>
                <AgendamentosList />
              </PrivateRoute>
            }
          />
          <Route
            path="/pacientes/:id/agendamentos/novo"
            element={
              <PrivateRoute roles={["SECRETARIA", "PROFISSIONAL_SAUDE"]}>
                <AgendamentoForm />
              </PrivateRoute>
            }
          />
          <Route
            path="/agendamentos/:id/editar"
            element={
              <PrivateRoute roles={["SECRETARIA", "PROFISSIONAL_SAUDE"]}>
                <AgendamentoForm />
              </PrivateRoute>
            }
          />
          <Route
            path="/consulta/:id"
            element={
              <PrivateRoute roles={["PROFISSIONAL_SAUDE"]}>
                <Consulta />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
