from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Agendamento, AgendamentoStatus
from pacientes.models import Paciente, Endereco
from usuarios.models import CustomUser, UserRole
import datetime

class AgendamentoAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.secretaria_user = CustomUser.objects.create_user(username='sec1', password='password', role=UserRole.SECRETARIA)
        cls.profissional_user = CustomUser.objects.create_user(username='prof1', password='password', role=UserRole.PROFISSIONAL_SAUDE)

        cls.endereco = Endereco.objects.create(cep='11111-000', uf='SP', cidade='Cidade Ag', logradouro='Rua Ag', numero='1', bairro='Bairro Ag')
        cls.paciente = Paciente.objects.create(
            cpf='123.456.789-00', nome='Paciente Ag', nascimento='1980-01-01',
            celular='11123456789', email='paciente.ag@example.com', endereco_residencial=cls.endereco, criado_por=cls.secretaria_user
        )
        cls.agendamento_url = reverse('agendamento-list') # basename 'agendamento'

    def setUp(self):
        self.client.force_authenticate(user=self.secretaria_user)

    def test_create_agendamento_valid_time(self):
        data = {
            'paciente_id': self.paciente.pk,
            'data': (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
            'hora': '10:00:00',
            'status': AgendamentoStatus.EM_ANDAMENTO
        }
        response = self.client.post(self.agendamento_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Agendamento.objects.count(), 1)
        ag = Agendamento.objects.first()
        self.assertEqual(ag.criado_por, self.secretaria_user)

    def test_create_agendamento_invalid_time_too_early(self):
        data = {'paciente_id': self.paciente.pk, 'data': (datetime.date.today()  + datetime.timedelta(days=1)).isoformat(), 'hora': '07:00:00'}
        response = self.client.post(self.agendamento_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hora', response.data)

    def test_create_agendamento_invalid_time_too_late(self):
        data = {'paciente_id': self.paciente.pk, 'data': (datetime.date.today()  + datetime.timedelta(days=1)).isoformat(), 'hora': '18:00:00'}
        response = self.client.post(self.agendamento_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('hora', response.data)

    def test_create_agendamento_conflict_paciente(self):
        existing_data = datetime.date.today() + datetime.timedelta(days=2)
        Agendamento.objects.create(
            paciente=self.paciente, data=existing_data, hora='14:00:00',
            criado_por=self.secretaria_user
        )
        data = {
            'paciente_id': self.paciente.pk,
            'data': existing_data.isoformat(), # Same date and time
            'hora': '14:00:00'
        }
        response = self.client.post(self.agendamento_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Due to unique_together or serializer validation
        # Check for specific error messages related to conflict
        self.assertTrue('detail' in response.data and "Paciente já possui um agendamento" in response.data['detail']
                        or 'non_field_errors' in response.data # Model's unique_together
                        or ('paciente_id' in response.data and any("conflito" in error for error in response.data['paciente_id']))
                        , response.data
                       )


    def test_create_agendamento_conflict_general_time(self):
        # Create agendamento for another paciente at the same time
        other_paciente_endereco = Endereco.objects.create(cep='99999-000', uf='RJ', cidade='Outra Cid', logradouro='Outra Rua', numero='99', bairro='Outro Bairro')
        other_paciente = Paciente.objects.create(cpf='987.654.321-00', nome='Outro Paciente Ag', endereco_residencial=other_paciente_endereco, nascimento='1990-01-01', email='other.ag@example.com', celular='12345678901', criado_por=self.secretaria_user)

        conflict_data_time = datetime.date.today() + datetime.timedelta(days=3)
        Agendamento.objects.create(
            paciente=other_paciente, data=conflict_data_time, hora='11:00:00',
            criado_por=self.secretaria_user
        )
        data = {
            'paciente_id': self.paciente.pk,
            'data': conflict_data_time.isoformat(), # Same date and time
            'hora': '11:00:00'
        }
        response = self.client.post(self.agendamento_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('detail' in response.data and "Já existe um agendamento para" in response.data['detail']
                        or 'non_field_errors' in response.data, response.data)


    def test_update_paciente_address_via_agendamento(self):
        ag_data = {
            'paciente_id': self.paciente.pk,
            'data': (datetime.date.today() + datetime.timedelta(days=4)).isoformat(),
            'hora': '15:00:00',
            # Address fields
            'endereco_residencial_logradouro': 'Nova Rua Teste',
            'endereco_residencial_numero': '123A',
            'endereco_residencial_cep': '11111-001' # New CEP
        }
        response = self.client.post(self.agendamento_url, ag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        self.paciente.refresh_from_db()
        # Important: The Paciente model's endereco_residencial is a ForeignKey.
        # The serializer updates the Endereco instance pointed to by this ForeignKey.
        updated_endereco = Endereco.objects.get(pk=self.paciente.endereco_residencial.pk)

        self.assertEqual(updated_endereco.logradouro, 'Nova Rua Teste')
        self.assertEqual(updated_endereco.numero, '123A')
        self.assertEqual(updated_endereco.cep, '11111-001')

        # Check audit fields on Agendamento
        ag = Agendamento.objects.get(pk=response.data['id'])
        self.assertEqual(ag.modificado_por, None)
        self.assertEqual(ag.criado_por, self.secretaria_user)
