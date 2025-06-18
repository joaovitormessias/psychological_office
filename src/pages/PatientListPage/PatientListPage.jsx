import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PatientService } from '../../services/PatientService';
import { Table, TableRow, Button, Spinner, Modal } from '../../components/common'; // Assuming common components are exported from common/index.js
import { showSuccessToast, showErrorToast } from '../../services/NotificationService';

const PatientListPage = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedPatientId, setSelectedPatientId] = useState(null);

  const fetchPatients = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await PatientService.getPatients();
      setPatients(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch patients.');
      showErrorToast(err.message || 'Failed to fetch patients.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const handleDeleteClick = (patientId) => {
    setSelectedPatientId(patientId);
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    if (!selectedPatientId) return;
    try {
      await PatientService.deletePatient(selectedPatientId);
      showSuccessToast('Patient deleted successfully!');
      fetchPatients(); // Refetch patients list
    } catch (err) {
      showErrorToast(err.message || 'Failed to delete patient.');
    } finally {
      setShowDeleteModal(false);
      setSelectedPatientId(null);
    }
  };

  const cancelDelete = () => {
    setShowDeleteModal(false);
    setSelectedPatientId(null);
  };

  const tableHeaders = ["Name", "CPF", "WhatsApp", "Email", "Status", "Actions"];

  if (loading) {
    return (
      <div className="p-4 flex justify-center items-center min-h-[calc(100vh-theme(spacing.32))]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <div className="p-4 text-red-500 text-center">Error: {error}</div>;
  }

  return (
    <div className="p-6 bg-gray-50 min-h-[calc(100vh-theme(spacing.32))]">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">Patient List</h1>
          <Button variant="primary" className="bg-green-500 hover:bg-green-700">
            <Link to="/patients/add">Add New Patient</Link>
          </Button>
        </div>

        {patients.length === 0 ? (
          <p className="text-center text-gray-500">No patients found.</p>
        ) : (
          <Table headers={tableHeaders} className="bg-white shadow-lg rounded-lg">
            {patients.map((patient) => (
              <TableRow key={patient.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{patient.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{patient.cpf}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {patient.whatsapp ? (
                    <a
                      href={`https://api.whatsapp.com/send/?phone=${patient.whatsapp.replace(/\D/g, '')}`} // Ensure only numbers
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800"
                    >
                      {patient.whatsapp}
                    </a>
                  ) : (
                    'N/A'
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{patient.email}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    patient.isActive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {patient.isActive ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <Link to={`/patients/edit/${patient.id}`} className="text-indigo-600 hover:text-indigo-900">Edit</Link>
                  <Button variant="outline_secondary" className="text-xs !py-1 !px-2 border-gray-400 text-gray-600 hover:bg-gray-400 hover:text-white" onClick={() => console.log("Schedule for", patient.id) /* Implement schedule link/action */}>
                    Schedule
                  </Button>
                  <Button variant="danger" className="text-xs !py-1 !px-2" onClick={() => handleDeleteClick(patient.id)}>
                    Delete
                  </Button>
                </td>
              </TableRow>
            ))}
          </Table>
        )}
      </div>

      <Modal
        isOpen={showDeleteModal}
        onClose={cancelDelete}
        title="Confirm Deletion"
        footerContent={
          <>
            <Button variant="secondary" onClick={cancelDelete} className="mr-2">Cancel</Button>
            <Button variant="danger" onClick={confirmDelete}>Delete Patient</Button>
          </>
        }
      >
        <p>Are you sure you want to delete this patient? This action cannot be undone.</p>
        {selectedPatientId && <p className="mt-2 text-sm text-gray-600">Patient: {patients.find(p=>p.id === selectedPatientId)?.name}</p>}
      </Modal>
    </div>
  );
};

export default PatientListPage;
