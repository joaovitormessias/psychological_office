from rest_framework import serializers
from django.db import transaction
from .models import Consulta
from agendamentos.models import Agendamento, AgendamentoStatus
from usuarios.models import UserRole # For checking role

class ConsultaSerializer(serializers.ModelSerializer):
    agendamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Agendamento.objects.filter(status=AgendamentoStatus.EM_ANDAMENTO, consulta__isnull=True),
        source='agendamento', write_only=True, label="ID do Agendamento"
    )
    paciente_nome = serializers.CharField(source='agendamento.paciente.nome', read_only=True)
    data_agendamento = serializers.DateField(source='agendamento.data', read_only=True)
    hora_agendamento = serializers.TimeField(source='agendamento.hora', read_only=True)
    profissional_responsavel_username = serializers.CharField(source='profissional_responsavel.username', read_only=True, allow_null=True)
    anotacoes_anteriores = serializers.CharField(read_only=True, allow_null=True)
    anotacoes_atuais = serializers.CharField()
    pontos_atencao = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    concluir_consulta = serializers.BooleanField(write_only=True, default=False, required=False)
    criado_por_username = serializers.CharField(source='criado_por.username', read_only=True, allow_null=True)
    modificado_por_username = serializers.CharField(source='modificado_por.username', read_only=True, allow_null=True)

    class Meta:
        model = Consulta
        fields = [
            'id', 'agendamento_id', 'paciente_nome', 'data_agendamento', 'hora_agendamento',
            'profissional_responsavel_username', 'anotacoes_anteriores', 'anotacoes_atuais',
            'pontos_atencao', 'concluir_consulta', 'criado_em', 'atualizado_em',
            'criado_por_username', 'modificado_por_username',
        ]
        read_only_fields = [
            'criado_em', 'atualizado_em', 'profissional_responsavel_username',
            'anotacoes_anteriores', 'criado_por_username', 'modificado_por_username'
        ]

    def _get_request_user(self):
        request = self.context.get('request')
        return request.user if request and hasattr(request, 'user') and request.user.is_authenticated else None

    def _handle_decryption_for_output(self, user, consulta_instance, field_name):
        raw_value = getattr(consulta_instance, field_name, None)
        if raw_value is None: return None
        if raw_value == "DECRYPTION_ERROR": return "Erro ao decifrar dado."

        # Ensure user is the professional responsible for this specific consultation to allow decryption
        if user and user.is_authenticated and user == consulta_instance.profissional_responsavel:
            return raw_value # Raw value is already decrypted by the custom field's from_db_value
        return "ACESSO RESTRITO"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = self._get_request_user()
        # Pass the instance itself to _handle_decryption_for_output
        ret['anotacoes_anteriores'] = self._handle_decryption_for_output(user, instance, 'anotacoes_anteriores')
        ret['anotacoes_atuais'] = self._handle_decryption_for_output(user, instance, 'anotacoes_atuais')
        ret['pontos_atencao'] = self._handle_decryption_for_output(user, instance, 'pontos_atencao')
        return ret

    def _get_previous_consultation_notes(self, paciente, current_agendamento_date):
        previous_consulta = Consulta.objects.filter(
            agendamento__paciente=paciente,
            agendamento__data__lt=current_agendamento_date,
        ).order_by('-agendamento__data', '-agendamento__hora').first()

        if previous_consulta:
            # Accessing the field directly will use the custom field's decryption logic
            notes = previous_consulta.anotacoes_atuais
            # The custom field returns "DECRYPTION_ERROR" if it fails, so we check for that
            return notes if notes != "DECRYPTION_ERROR" else "Erro ao carregar anotações anteriores."
        return None

    @transaction.atomic
    def create(self, validated_data):
        user = self._get_request_user()
        if not (user and user.role == UserRole.PROFISSIONAL_SAUDE):
             raise serializers.ValidationError({"detail": "Apenas Profissionais de Saúde podem registrar consultas."})

        validated_data['profissional_responsavel'] = user
        validated_data['criado_por'] = user
        agendamento = validated_data['agendamento']

        # Fetch previous notes using the custom field's decryption
        previous_notes = self._get_previous_consultation_notes(agendamento.paciente, agendamento.data)
        validated_data['anotacoes_anteriores'] = previous_notes

        concluir = validated_data.pop('concluir_consulta', False)
        consulta = Consulta.objects.create(**validated_data)

        if concluir:
            agendamento.status = AgendamentoStatus.CONCLUIDO
            agendamento.modificado_por = user # Audit the change to agendamento
            agendamento.save(update_fields=['status', 'modificado_por', 'atualizado_em'])
        return consulta

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self._get_request_user()
        if not user or user != instance.profissional_responsavel: # Check against the instance's professional
            raise serializers.ValidationError({"detail": "Você não tem permissão para editar esta consulta."})

        validated_data['modificado_por'] = user
        # These fields should not be changed during an update via this serializer
        validated_data.pop('anotacoes_anteriores', None)
        validated_data.pop('profissional_responsavel', None)
        validated_data.pop('agendamento', None) # Agendamento is fixed once consulta is created

        concluir = validated_data.pop('concluir_consulta', False)

        # Perform the update on the instance fields
        instance = super().update(instance, validated_data)

        if concluir and instance.agendamento.status != AgendamentoStatus.CONCLUIDO:
            instance.agendamento.status = AgendamentoStatus.CONCLUIDO
            instance.agendamento.modificado_por = user # Audit the change to agendamento
            instance.agendamento.save(update_fields=['status', 'modificado_por', 'atualizado_em'])
        return instance
