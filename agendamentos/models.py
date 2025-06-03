from django.db import models
from django.conf import settings
from pacientes.models import Paciente, TimeStampedModel # Assuming TimeStampedModel is here
from django.core.exceptions import ValidationError
import datetime

class AgendamentoStatus(models.TextChoices):
    EM_ANDAMENTO = 'EM_ANDAMENTO', 'Em andamento'
    CONCLUIDO = 'CONCLUIDO', 'Concluído'
    CANCELADO = 'CANCELADO', 'Cancelado' # Adding a common status

class Agendamento(TimeStampedModel):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=AgendamentoStatus.choices,
        default=AgendamentoStatus.EM_ANDAMENTO
    )
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['data', 'hora']
        unique_together = [['paciente', 'data', 'hora'], ['data', 'hora']] # Prevent patient double booking and general double booking if only one professional context

    def __str__(self):
        return f"Agendamento para {self.paciente.nome} em {self.data} às {self.hora}"

    def clean(self):
        super().clean()
        # Validate appointment time (08h-17h)
        if not (datetime.time(8, 0) <= self.hora <= datetime.time(17, 0)):
            raise ValidationError({'hora': 'Agendamentos devem ser entre 08:00 e 17:00.'})

        # Basic conflict check (already handled by unique_together for new instances)
        # For updates, unique_together also helps. More complex logic might be needed
        # if, for example, professionals are involved.
        # The unique_together constraint ['data', 'hora'] implies a single professional context.
        # If multiple professionals, this constraint would need to be ['data', 'hora', 'profissional']

        # Check if date is in the past (optional, but good practice for new appointments)
        # if self.data < datetime.date.today() and not self.pk: # Only for new instances
        #     raise ValidationError({'data': 'Não é possível criar agendamentos para datas passadas.'})
