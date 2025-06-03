from django.db import models
from django.conf import settings
from pacientes.models import TimeStampedModel
from agendamentos.models import Agendamento
from core.fields import EncryptedTextField

class Consulta(TimeStampedModel):
    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.PROTECT,
        related_name='consulta'
    )
    profissional_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='consultas_realizadas'
    )
    anotacoes_anteriores = EncryptedTextField(blank=True, null=True)
    anotacoes_atuais = EncryptedTextField()
    pontos_atencao = EncryptedTextField(blank=True, null=True)

    def __str__(self):
        return f"Consulta para {self.agendamento.paciente.nome} em {self.agendamento.data} por {self.profissional_responsavel.username}"

    class Meta:
        ordering = ['-agendamento__data', '-agendamento__hora']
