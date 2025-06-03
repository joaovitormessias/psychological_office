from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Consulta
from agendamentos.models import Agendamento, AgendamentoStatus
from pacientes.models import Paciente, Endereco
from usuarios.models import CustomUser, UserRole
import datetime

# Mock settings.FERNET_KEY for tests if it's not already configured robustly for test environment
# Ensure the key used for tests is consistent if you need to decrypt values manually for asserts.
# The EncryptedTextField should handle encryption/decryption transparently if key is good.

class ConsultaAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prof_user1 = CustomUser.objects.create_user(username='prof_consulta1', password='password', role=UserRole.PROFISSIONAL_SAUDE)
        cls.prof_user2 = CustomUser.objects.create_user(username='prof_consulta2', password='password', role=UserRole.PROFISSIONAL_SAUDE)
        cls.secretaria_user = CustomUser.objects.create_user(username='sec_consulta', password='password', role=UserRole.SECRETARIA)

        cls.endereco = Endereco.objects.create(cep='22222-000', uf='RJ', cidade='Rio Teste', logradouro='Av Teste', numero='100', bairro='Bairro Consulta')
        cls.paciente = Paciente.objects.create(
            cpf='777.777.777-77', nome='Paciente Consulta', nascimento='1970-01-01',
            celular='21999990000', email='paciente.consulta@example.com', endereco_residencial=cls.endereco, criado_por=cls.secretaria_user # Assuming secretaria can create patient
        )

        # Agendamento 1 for prof_user1 (previous, will be base for anotacoes_anteriores)
        cls.agendamento1_prev_date = datetime.date.today() - datetime.timedelta(days=10)
        cls.agendamento1_prev = Agendamento.objects.create(
            paciente=cls.paciente, data=cls.agendamento1_prev_date, hora='10:00:00',
            status=AgendamentoStatus.CONCLUIDO, criado_por=cls.prof_user1
        )
        cls.consulta1_prev_notes = "Notas da consulta anterior."
        cls.consulta1_prev = Consulta.objects.create(
            agendamento=cls.agendamento1_prev, profissional_responsavel=cls.prof_user1,
            anotacoes_atuais=cls.consulta1_prev_notes, pontos_atencao="Ponto anterior.", criado_por=cls.prof_user1
        )

        # Agendamento 2 for prof_user1 (current one to create consulta for)
        cls.agendamento2_curr_date = datetime.date.today() + datetime.timedelta(days=1)
        cls.agendamento2_curr = Agendamento.objects.create(
            paciente=cls.paciente, data=cls.agendamento2_curr_date, hora='11:00:00',
            status=AgendamentoStatus.EM_ANDAMENTO, criado_por=cls.prof_user1
        )

        # Agendamento 3 for prof_user2
        cls.agendamento3_other_prof_date = datetime.date.today() + datetime.timedelta(days=2)
        cls.agendamento3_other_prof = Agendamento.objects.create(
            paciente=cls.paciente, data=cls.agendamento3_other_prof_date, hora='12:00:00',
            status=AgendamentoStatus.EM_ANDAMENTO, criado_por=cls.prof_user2
        )

        cls.consulta_url = reverse('consulta-list') # basename 'consulta'

    def setUp(self):
        self.client.force_authenticate(user=self.prof_user1)

    def test_create_consulta(self):
        data = {
            'agendamento_id': self.agendamento2_curr.pk,
            'anotacoes_atuais': "Anotações da consulta atual.",
            'pontos_atencao': "Pontos de atenção atuais.",
            'concluir_consulta': False
        }
        response = self.client.post(self.consulta_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        # self.assertEqual(Consulta.objects.count(), 2) # Including consulta1_prev

        consulta = Consulta.objects.get(agendamento=self.agendamento2_curr)
        self.assertEqual(consulta.profissional_responsavel, self.prof_user1)
        self.assertEqual(consulta.anotacoes_atuais, "Anotações da consulta atual.")
        self.assertEqual(consulta.anotacoes_anteriores, self.consulta1_prev_notes)
        self.assertEqual(consulta.criado_por, self.prof_user1)
        self.agendamento2_curr.refresh_from_db()
        self.assertEqual(self.agendamento2_curr.status, AgendamentoStatus.EM_ANDAMENTO)

        self.assertEqual(response.data['anotacoes_atuais'], "Anotações da consulta atual.")
        self.assertEqual(response.data['anotacoes_anteriores'], self.consulta1_prev_notes)


    def test_create_consulta_and_conclude_agendamento(self):
        data = {
            'agendamento_id': self.agendamento2_curr.pk,
            'anotacoes_atuais': "Consulta para concluir.",
            'concluir_consulta': True
        }
        # Ensure agendamento2_curr is not already associated with a consulta
        if hasattr(self.agendamento2_curr, 'consulta'):
            self.agendamento2_curr.consulta.delete()

        response = self.client.post(self.consulta_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        self.agendamento2_curr.refresh_from_db()
        self.assertEqual(self.agendamento2_curr.status, AgendamentoStatus.CONCLUIDO)
        self.assertEqual(self.agendamento2_curr.modificado_por, self.prof_user1)


    def test_consulta_access_denied_for_secretaria(self):
        self.client.force_authenticate(user=self.secretaria_user)
        response = self.client.get(self.consulta_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profissional_sees_only_own_consultas_list(self):
        # prof_user1 already has consulta1_prev
        # Create another one for prof_user1 if agendamento2_curr is not yet used
        if not Consulta.objects.filter(agendamento=self.agendamento2_curr).exists():
            Consulta.objects.create(agendamento=self.agendamento2_curr, profissional_responsavel=self.prof_user1, anotacoes_atuais="P1 notes")

        # prof_user2 creates a consulta
        if not Consulta.objects.filter(agendamento=self.agendamento3_other_prof).exists():
            Consulta.objects.create(agendamento=self.agendamento3_other_prof, profissional_responsavel=self.prof_user2, anotacoes_atuais="P2 notes")

        self.client.force_authenticate(user=self.prof_user1)
        response = self.client.get(self.consulta_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_count = Consulta.objects.filter(profissional_responsavel=self.prof_user1).count()
        self.assertEqual(len(response.data), expected_count)
        for c_data in response.data:
            self.assertEqual(c_data['profissional_responsavel_username'], self.prof_user1.username)

    def test_profissional_cannot_see_other_prof_consulta_detail_decrypted(self):
        detail_url = reverse('consulta-detail', kwargs={'pk': self.consulta1_prev.pk}) # Belongs to prof_user1
        self.client.force_authenticate(user=self.prof_user2)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Viewset's get_queryset filters

    def test_retrieve_own_consulta_decrypted(self):
        detail_url = reverse('consulta-detail', kwargs={'pk': self.consulta1_prev.pk})
        self.client.force_authenticate(user=self.prof_user1)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['anotacoes_atuais'], self.consulta1_prev.anotacoes_atuais)
        self.assertEqual(response.data['pontos_atencao'], self.consulta1_prev.pontos_atencao)


    def test_update_own_consulta(self):
        # Ensure agendamento2_curr does not have a consulta yet, or use a new one
        if hasattr(self.agendamento2_curr, 'consulta'):
             self.agendamento2_curr.consulta.delete()

        consulta_to_update = Consulta.objects.create(
            agendamento=self.agendamento2_curr, profissional_responsavel=self.prof_user1,
            anotacoes_atuais="Initial notes for update.", criado_por=self.prof_user1
        )
        detail_url = reverse('consulta-detail', kwargs={'pk': consulta_to_update.pk})
        update_data = {
            'anotacoes_atuais': "Updated notes.",
            'pontos_atencao': "Updated points.",
            'concluir_consulta': True
        }
        response = self.client.patch(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        consulta_to_update.refresh_from_db()
        self.assertEqual(consulta_to_update.anotacoes_atuais, "Updated notes.")
        self.assertEqual(consulta_to_update.modificado_por, self.prof_user1)

        self.agendamento2_curr.refresh_from_db()
        self.assertEqual(self.agendamento2_curr.status, AgendamentoStatus.CONCLUIDO)
