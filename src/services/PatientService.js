// src/services/PatientService.js
const mockPatients = [
  { id: '1', name: 'Alice Wonderland', cpf: '111.111.111-11', dateOfBirth: '1990-05-15', whatsapp: '5511987654321', email: 'alice@example.com', isActive: true, address: { street: '123 Main St', city: 'Anytown', zip: '12345', state: 'CA' }, billingAddress: { street: '123 Main St', city: 'Anytown', zip: '12345', state: 'CA' } },
  { id: '2', name: 'Bob The Builder', cpf: '222.222.222-22', dateOfBirth: '1985-10-20', whatsapp: '5521912345678', email: 'bob@example.com', isActive: true, address: { street: '456 Oak Ave', city: 'Otherville', zip: '67890', state: 'NY' }, billingAddress: { street: '456 Oak Ave', city: 'Otherville', zip: '67890', state: 'NY' } },
  { id: '3', name: 'Charlie Brown', cpf: '333.333.333-33', dateOfBirth: '2000-01-30', whatsapp: '5531988887777', email: 'charlie@example.com', isActive: false, address: { street: '789 Pine Ln', city: 'Smalltown', zip: '10111', state: 'TX' }, billingAddress: { street: '789 Pine Ln', city: 'Smalltown', zip: '10111', state: 'TX' } },
];

export const PatientService = {
  getPatients: async () => {
    console.log("PatientService: Fetching mock patients...");
    return new Promise(resolve => {
      setTimeout(() => {
        // Sort alphabetically by name for the RQF2 requirement
        const sortedPatients = [...mockPatients].sort((a, b) => a.name.localeCompare(b.name));
        resolve(sortedPatients);
      }, 500);
    });
  },
  // deletePatient will be added later
  deletePatient: async (patientId) => {
    console.log(`PatientService: Deleting patient with id ${patientId}`);
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const index = mockPatients.findIndex(p => p.id === patientId);
        if (index > -1) {
          // mockPatients.splice(index, 1); // This would modify the original array affecting subsequent getPatients calls in a mock setup
          console.log(`Mock: Patient ${patientId} "deleted". In a real app, this would be an API call.`);
          resolve({ message: 'Patient deleted successfully' });
        } else {
          reject(new Error('Patient not found'));
        }
      }, 500);
    });
  }
};
