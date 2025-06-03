from django.db import models
from django.conf import settings # To link to CustomUser for audit fields
from usuarios.models import CustomUser # Explicit import for clarity

# It's good practice to have a base model for audit fields
class TimeStampedModel(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_criado_por'
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_modificado_por'
    )

    class Meta:
        abstract = True

class Endereco(models.Model): # Not inheriting TimeStampedModel as it's part of Paciente
    cep = models.CharField(max_length=9) # Formato XXXXX-XXX
    uf = models.CharField(max_length=2) # Sigla do estado
    cidade = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20, default='SN') # Pode ser 'SN'
    bairro = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.uf}"

class Paciente(TimeStampedModel):
    cpf = models.CharField(max_length=14, unique=True) # Formato XXX.XXX.XXX-XX
    nome = models.CharField(max_length=255)
    nascimento = models.DateField()

    endereco_residencial = models.ForeignKey(
        Endereco,
        on_delete=models.PROTECT, # Or models.SET_NULL, depending on desired behavior
        related_name='pacientes_residencial'
    )
    # endereco_cobranca can be null if it's the same as residencial
    endereco_cobranca = models.ForeignKey(
        Endereco,
        on_delete=models.PROTECT, # Or models.SET_NULL
        related_name='pacientes_cobranca',
        null=True,
        blank=True
    )

    whatsapp = models.CharField(max_length=20, blank=True) # e.g., +55119XXXXXXXX
    celular = models.CharField(max_length=20) # Obrigatório
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Ensure CPF format if needed (basic validation, more complex can be in forms/serializers)
        # Ensure WhatsApp format if needed

        # If endereco_cobranca is not provided, it implies it's the same as residencial.
        # However, the requirement is "Possibilidade de repetir endereço domiciliar para cobrança."
        # This usually means a checkbox in the UI "Billing address same as home address".
        # If that checkbox is ticked, the frontend would copy the residential address data
        # to the billing address fields OR we handle it here by creating a new Endereco instance.
        # For now, the model allows endereco_cobranca to be null, or point to a different Endereco.
        # If it should be a distinct copy, the creation logic is in the serializer/view.
        super().save(*args, **kwargs)
