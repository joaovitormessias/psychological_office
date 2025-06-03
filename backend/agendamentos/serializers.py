from rest_framework import serializers
from .models import Agendamento, AgendamentoStatus
from pacientes.models import Paciente, Endereco
from pacientes.serializers import EnderecoSerializer # For address updates
from django.db import transaction
import datetime

class AgendamentoSerializer(serializers.ModelSerializer):
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.all(),
        source='paciente',
        write_only=True,
        label="ID do Paciente"
    )
    # Display patient name for readability
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)

    # Fields for updating Paciente's Endereco Residencial (optional)
    # These are write-only and not part of the Agendamento model itself
    endereco_residencial_cep = serializers.CharField(write_only=True, required=False, allow_blank=True)
    endereco_residencial_logradouro = serializers.CharField(write_only=True, required=False, allow_blank=True)
    endereco_residencial_numero = serializers.CharField(write_only=True, required=False, allow_blank=True)
    endereco_residencial_bairro = serializers.CharField(write_only=True, required=False, allow_blank=True)
    endereco_residencial_cidade = serializers.CharField(write_only=True, required=False, allow_blank=True)
    endereco_residencial_uf = serializers.CharField(write_only=True, required=False, allow_blank=True)

    # Audit fields from TimeStampedModel
    criado_por_username = serializers.CharField(source='criado_por.username', read_only=True, allow_null=True)
    modificado_por_username = serializers.CharField(source='modificado_por.username', read_only=True, allow_null=True)


    class Meta:
        model = Agendamento
        fields = [
            'id', 'paciente_id', 'paciente_nome', 'data', 'hora', 'status', 'observacoes',
            'criado_em', 'atualizado_em', 'criado_por_username', 'modificado_por_username',
            # Address fields for potential update
            'endereco_residencial_cep', 'endereco_residencial_logradouro',
            'endereco_residencial_numero', 'endereco_residencial_bairro',
            'endereco_residencial_cidade', 'endereco_residencial_uf',
        ]
        read_only_fields = ['criado_em', 'atualizado_em', 'criado_por_username', 'modificado_por_username']

    def validate_hora(self, value):
        # Rule: Datas entre 08h e 17h apenas
        if not (datetime.time(8, 0) <= value <= datetime.time(17, 0)):
            raise serializers.ValidationError("Agendamentos devem ser entre 08:00 e 17:00.")
        return value

    def validate(self, data):
        # Rule: Sem conflito de horários
        # unique_together in model handles this for (<paciente>, data, hora) and (data, hora)
        # This validation is an additional check, especially for updates.

        paciente = data.get('paciente') # This will be the Paciente instance from paciente_id
        data_ag = data.get('data')
        hora_ag = data.get('hora')

        # On create
        if not self.instance:
            # Check for patient conflict
            if Agendamento.objects.filter(paciente=paciente, data=data_ag, hora=hora_ag).exists():
                raise serializers.ValidationError(
                    {"detail": f"Paciente já possui um agendamento para {data_ag} às {hora_ag}."}
                )
            # Check for general conflict (assuming single professional context)
            if Agendamento.objects.filter(data=data_ag, hora=hora_ag).exists():
                raise serializers.ValidationError(
                    {"detail": f"Já existe um agendamento para {data_ag} às {hora_ag}."}
                )
        # On update
        else:
            # Check for patient conflict (excluding self)
            if Agendamento.objects.filter(paciente=paciente, data=data_ag, hora=hora_ag).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(
                    {"detail": f"Paciente já possui outro agendamento para {data_ag} às {hora_ag}."}
                )
            # Check for general conflict (excluding self)
            if Agendamento.objects.filter(data=data_ag, hora=hora_ag).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(
                    {"detail": f"Já existe outro agendamento para {data_ag} às {hora_ag}."}
                )

        # Rule: Dados do cliente não podem ser alterados na tela de agendamento.
        # This is handled by using paciente_id (PK) for write and paciente_nome for read.
        # The address update is an exception to this rule as per "Endereço pode ser atualizado."

        return data

    def _update_paciente_endereco(self, paciente, validated_data):
        # Helper to update paciente's residential address if fields are provided
        endereco_data = {
            'cep': validated_data.get('endereco_residencial_cep'),
            'logradouro': validated_data.get('endereco_residencial_logradouro'),
            'numero': validated_data.get('endereco_residencial_numero'),
            'bairro': validated_data.get('endereco_residencial_bairro'),
            'cidade': validated_data.get('endereco_residencial_cidade'),
            'uf': validated_data.get('endereco_residencial_uf'),
        }
        # Filter out None values so partial updates work correctly with EnderecoSerializer
        endereco_data_cleaned = {k: v for k, v in endereco_data.items() if v is not None and v != ''}

        if not endereco_data_cleaned:
            return False # No address data to update

        if paciente.endereco_residencial:
            endereco_serializer = EnderecoSerializer(
                paciente.endereco_residencial, data=endereco_data_cleaned, partial=True
            )
        else: # Should not happen if Paciente always has a residential address
            endereco_serializer = EnderecoSerializer(data=endereco_data_cleaned)

        if endereco_serializer.is_valid(raise_exception=True):
            endereco_serializer.save()
            # If paciente.endereco_residencial was null and new one created
            if not paciente.endereco_residencial:
                paciente.endereco_residencial = endereco_serializer.instance
                paciente.save(update_fields=['endereco_residencial'])
            return True
        return False


    def create(self, validated_data):
        with transaction.atomic():
            paciente = validated_data.get('paciente') # Already a Paciente instance due to source='paciente'

            # Handle address update before creating agendamento
            address_fields_present = any(
                validated_data.get(f"endereco_residencial_{field}") for field in ['cep', 'logradouro', 'numero', 'bairro', 'cidade', 'uf']
            )
            if address_fields_present:
                 self._update_paciente_endereco(paciente, {
                    'endereco_residencial_cep': validated_data.pop('endereco_residencial_cep', None),
                    'endereco_residencial_logradouro': validated_data.pop('endereco_residencial_logradouro', None),
                    'endereco_residencial_numero': validated_data.pop('endereco_residencial_numero', None),
                    'endereco_residencial_bairro': validated_data.pop('endereco_residencial_bairro', None),
                    'endereco_residencial_cidade': validated_data.pop('endereco_residencial_cidade', None),
                    'endereco_residencial_uf': validated_data.pop('endereco_residencial_uf', None),
                })
            else: # Remove address keys if not present to avoid issues with model creation
                validated_data.pop('endereco_residencial_cep', None)
                validated_data.pop('endereco_residencial_logradouro', None)
                validated_data.pop('endereco_residencial_numero', None)
                validated_data.pop('endereco_residencial_bairro', None)
                validated_data.pop('endereco_residencial_cidade', None)
                validated_data.pop('endereco_residencial_uf', None)

            # Set criado_por
            request = self.context.get('request')
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                validated_data['criado_por'] = request.user

            agendamento = Agendamento.objects.create(**validated_data)
            return agendamento

    def update(self, instance, validated_data):
        with transaction.atomic():
            paciente = validated_data.get('paciente', instance.paciente)

            # Handle address update
            address_fields_present = any(
                validated_data.get(f"endereco_residencial_{field}") for field in ['cep', 'logradouro', 'numero', 'bairro', 'cidade', 'uf']
            )
            if address_fields_present:
                self._update_paciente_endereco(paciente, {
                    'endereco_residencial_cep': validated_data.pop('endereco_residencial_cep', None),
                    'endereco_residencial_logradouro': validated_data.pop('endereco_residencial_logradouro', None),
                    'endereco_residencial_numero': validated_data.pop('endereco_residencial_numero', None),
                    'endereco_residencial_bairro': validated_data.pop('endereco_residencial_bairro', None),
                    'endereco_residencial_cidade': validated_data.pop('endereco_residencial_cidade', None),
                    'endereco_residencial_uf': validated_data.pop('endereco_residencial_uf', None),
                })
            else: # Remove address keys if not present
                validated_data.pop('endereco_residencial_cep', None)
                validated_data.pop('endereco_residencial_logradouro', None)
                validated_data.pop('endereco_residencial_numero', None)
                validated_data.pop('endereco_residencial_bairro', None)
                validated_data.pop('endereco_residencial_cidade', None)
                validated_data.pop('endereco_residencial_uf', None)


            # Set modificado_por
            request = self.context.get('request')
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                validated_data['modificado_por'] = request.user

            # Update Agendamento fields
            # Need to pop 'paciente' if it's in validated_data as it's already handled or taken from instance
            validated_data.pop('paciente', None)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()
            return instance
