from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Paciente, Endereco
from usuarios.models import CustomUser, UserRole
import datetime

class PacienteAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.secretaria_user = CustomUser.objects.create_user(username='testsecretaria', password='password', role=UserRole.SECRETARIA)
        cls.profissional_user = CustomUser.objects.create_user(username='testprof', password='password', role=UserRole.PROFISSIONAL_SAUDE)
        cls.other_user = CustomUser.objects.create_user(username='otheruser', password='password', role=UserRole.ADMIN) # A user that shouldn't have access

        cls.endereco_data1 = {'cep': '12345-001', 'uf': 'SP', 'cidade': 'Cidade Teste1', 'logradouro': 'Rua Teste1', 'numero': '101', 'bairro': 'Bairro Teste1'}
        cls.endereco1 = Endereco.objects.create(**cls.endereco_data1)

        cls.paciente_url = reverse('paciente-list') # Assumes basename 'paciente' from router registration

    def setUp(self):
        # Authenticate as secretaria by default for most tests
        self.client.force_authenticate(user=self.secretaria_user)

    def test_create_paciente_with_residential_address_only(self):
        paciente_data = {
            'cpf': '111.111.111-11',
            'nome': 'Paciente Um',
            'nascimento': '1990-01-01',
            'celular': '11999999999',
            'email': 'paciente1@example.com',
            'endereco_residencial': self.endereco_data1,
            # endereco_cobranca is optional
        }
        response = self.client.post(self.paciente_url, paciente_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Paciente.objects.count(), 1)
        paciente = Paciente.objects.first()
        self.assertEqual(paciente.nome, 'Paciente Um')
        self.assertIsNotNone(paciente.endereco_residencial)
        self.assertIsNone(paciente.endereco_cobranca) # Should be None as it wasn't provided
        self.assertEqual(paciente.criado_por, self.secretaria_user)
        self.assertTrue(response.data['whatsapp_link'] is None)


    def test_create_paciente_with_billing_same_as_residential(self):
        paciente_data = {
            'cpf': '222.222.222-22',
            'nome': 'Paciente Dois',
            'nascimento': '1992-02-02',
            'celular': '11988888888',
            'email': 'paciente2@example.com',
            'whatsapp': '5511988888888',
            'endereco_residencial': self.endereco_data1,
            'repetir_endereco_cobranca': True
        }
        response = self.client.post(self.paciente_url, paciente_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        paciente = Paciente.objects.get(cpf='222.222.222-22')
        self.assertIsNotNone(paciente.endereco_residencial)
        self.assertEqual(paciente.endereco_cobranca, paciente.endereco_residencial)
        self.assertIn('https://wa.me/5511988888888', response.data['whatsapp_link'])


    def test_create_paciente_with_different_billing_address(self):
        endereco_data_cobranca = {'cep': '54321-000', 'uf': 'RJ', 'cidade': 'Outra Cidade', 'logradouro': 'Outra Rua', 'numero': '202', 'bairro': 'Outro Bairro'}
        paciente_data = {
            'cpf': '333.333.333-33',
            'nome': 'Paciente Tres',
            'nascimento': '1993-03-03',
            'celular': '11977777777',
            'email': 'paciente3@example.com',
            'endereco_residencial': self.endereco_data1,
            'endereco_cobranca': endereco_data_cobranca,
            'repetir_endereco_cobranca': False
        }
        response = self.client.post(self.paciente_url, paciente_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        paciente = Paciente.objects.get(cpf='333.333.333-33')
        self.assertNotEqual(paciente.endereco_cobranca, paciente.endereco_residencial)
        self.assertEqual(paciente.endereco_cobranca.cep, '54321-000')

    def test_update_paciente_cannot_update_cpf(self):
        paciente = Paciente.objects.create(
            cpf='444.444.444-44', nome='Paciente Quatro', nascimento='1994-04-04',
            celular='11966666666', email='paciente4@example.com',
            endereco_residencial=self.endereco1, criado_por=self.secretaria_user
        )
        update_data = {'nome': 'Paciente Quatro Atualizado', 'cpf': '000.000.000-00'}
        # Use reverse with pk for detail URL
        detail_url = reverse('paciente-detail', kwargs={'pk': paciente.pk})
        response = self.client.patch(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        paciente.refresh_from_db()
        self.assertEqual(paciente.nome, 'Paciente Quatro Atualizado')
        self.assertEqual(paciente.cpf, '444.444.444-44') # CPF should not change
        self.assertEqual(paciente.modificado_por, self.secretaria_user)

    def test_paciente_access_by_profissional_saude(self):
        self.client.force_authenticate(user=self.profissional_user)
        response = self.client.get(self.paciente_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_paciente_access_denied_for_other_roles(self):
        self.client.force_authenticate(user=self.other_user) # e.g. an admin without explicit grant
        response = self.client.get(self.paciente_url)
        # This depends on IsSecretaria | IsProfissionalSaude. Admin is not in this set.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_pacientes_ordered_alphabetically(self):
        Paciente.objects.create(cpf='999.999.999-99', nome='Zulu', nascimento='2000-01-01', celular='1234567890', email='zulu@example.com', endereco_residencial=self.endereco1, criado_por=self.secretaria_user)
        Paciente.objects.create(cpf='888.888.888-88', nome='Alpha', nascimento='2000-01-01', celular='0987654321', email='alpha@example.com', endereco_residencial=self.endereco1, criado_por=self.secretaria_user)
        response = self.client.get(self.paciente_url) # Gets all pacientes
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure there are enough patients to test ordering
        self.assertTrue(len(response.data) >= 2)

        # Extract names from response data
        names = [p['nome'] for p in response.data]
        # Check if 'Alpha' comes before 'Zulu' in the list
        # This depends on the number of pre-existing patients and their names.
        # A more robust test would be to ensure the list is sorted.
        self.assertEqual(names, sorted(names))
        # If specifically want to check Alpha then Zulu (assuming these are the only two or first two after sorting)
        if 'Alpha' in names and 'Zulu' in names:
             self.assertLess(names.index('Alpha'), names.index('Zulu'))
