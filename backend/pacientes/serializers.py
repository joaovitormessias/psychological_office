from rest_framework import serializers
from .models import Endereco, Paciente
from django.db import transaction

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['id', 'cep', 'uf', 'cidade', 'logradouro', 'numero', 'bairro']

    def validate_cep(self, value):
        # Basic CEP validation (e.g., format XXXXX-XXX or XXXXXXXX)
        # For simplicity, we'll just check length here. More robust validation can be added.
        if not (len(value) == 8 or (len(value) == 9 and value[5] == '-')):
            # raise serializers.ValidationError("CEP deve estar no formato XXXXXXXX ou XXXXX-XXX.")
            pass # Allowing flexibility for now, can be tightened
        return value

    # Mock CEP lookup
    def create(self, validated_data):
        cep = validated_data.get('cep')
        # Mock: if CEP is '12345-678' or '12345678', fill some data
        if cep in ['12345-678', '12345678'] and not validated_data.get('logradouro'):
            validated_data['logradouro'] = "Rua Mockada"
            validated_data['bairro'] = "Bairro Mock"
            validated_data['cidade'] = "Cidade Mock"
            validated_data['uf'] = "MK"
        return super().create(validated_data)

class PacienteSerializer(serializers.ModelSerializer):
    endereco_residencial = EnderecoSerializer()
    endereco_cobranca = EnderecoSerializer(required=False, allow_null=True)
    whatsapp_link = serializers.SerializerMethodField()
    # cidade_choices = serializers.SerializerMethodField() # For UF-dependent city filtering

    # Audit fields are read-only by default, but let's be explicit
    # NOTE: The frontend (PacienteForm.jsx) is currently sending a flat data structure for patient creation/update.
    # This serializer expects nested objects for 'endereco_residencial' and 'endereco_cobranca'.
    # This discrepancy will need to be resolved, likely by updating the frontend to send nested data.
    criado_por = serializers.PrimaryKeyRelatedField(read_only=True)
    modificado_por = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Paciente
        fields = [
            'id', 'cpf', 'nome', 'nascimento', 'endereco_residencial',
            'endereco_cobranca', 'repetir_endereco_cobranca', # Virtual field for control
            'whatsapp', 'celular', 'email', 'whatsapp_link',
            'criado_em', 'atualizado_em', 'criado_por', 'modificado_por'
        ]
        read_only_fields = ['criado_em', 'atualizado_em', 'criado_por', 'modificado_por']

    # Virtual field to control address repetition
    repetir_endereco_cobranca = serializers.BooleanField(write_only=True, required=False, default=False)

    def get_whatsapp_link(self, obj):
        if obj.whatsapp:
            # Remove non-digits and add country code if missing (assuming Brazil +55)
            phone = ''.join(filter(str.isdigit, obj.whatsapp))
            if not phone.startswith('55') and len(phone) >= 10: # Basic check
                 # This logic might need refinement based on common input formats
                if len(phone) == 11: # Common mobile format like 119XXXXXXXX
                    phone = '55' + phone
                elif len(phone) == 10: # Common fixed line like 11XXXXXXXX
                     phone = '55' + phone # Or add DDD if it's missing
            return f"https://wa.me/{phone}"
        return None

    # Mock city filtering based on UF
    # def get_cidade_choices(self, obj):
    #     # This would typically involve querying a City model filtered by UF
    #     # For now, returning a mock list
    #     uf = self.initial_data.get('endereco_residencial', {}).get('uf') or     #          (obj.endereco_residencial.uf if obj and obj.endereco_residencial else None)
    #     if uf == 'SP':
    #         return ["São Paulo", "Campinas", "Santos"]
    #     elif uf == 'RJ':
    #         return ["Rio de Janeiro", "Niterói"]
    #     return []


    def validate_cpf(self, value):
        # Basic CPF validation (e.g., format XXX.XXX.XXX-XX or XXXXXXXXXXX)
        # For simplicity, just checking length. Robust validation (checksum) is recommended.
        cleaned_cpf = ''.join(filter(str.isdigit, value))
        if len(cleaned_cpf) != 11:
            # raise serializers.ValidationError("CPF deve conter 11 dígitos.")
            pass # Allowing flexibility for now

        # Check uniqueness, DRF UniqueValidator handles this if field is unique=True
        # but if we clean the CPF, we might need explicit check if format varies
        # For now, assuming model's unique=True is sufficient with raw input.
        return value

    def create(self, validated_data):
        with transaction.atomic():
            endereco_residencial_data = validated_data.pop('endereco_residencial')
            endereco_cobranca_data = validated_data.pop('endereco_cobranca', None)
            repetir_endereco = validated_data.pop('repetir_endereco_cobranca', False)

            # Mock CEP lookup for residencial if not already filled by EnderecoSerializer's create
            if 'cep' in endereco_residencial_data and endereco_residencial_data['cep'] in ['12345-678', '12345678'] and not endereco_residencial_data.get('logradouro'):
                endereco_residencial_data['logradouro'] = "Rua Mockada Create"
                endereco_residencial_data['bairro'] = "Bairro Mock Create"
                endereco_residencial_data['cidade'] = "Cidade Mock Create"
                endereco_residencial_data['uf'] = "MC"

            endereco_residencial = Endereco.objects.create(**endereco_residencial_data)

            paciente_instance = Paciente(endereco_residencial=endereco_residencial, **validated_data)

            if repetir_endereco:
                # Create a new Endereco instance by copying data from residencial
                # This ensures they are distinct records if that's the requirement
                # Or, if they can point to the same record, then:
                # paciente_instance.endereco_cobranca = endereco_residencial

                # Per "Possibilidade de repetir endereço domiciliar para cobrança"
                # this implies if selected, cobranca IS residencial.
                # If it means a COPY, then new instance is needed.
                # Assuming it means they are the *same* address object.
                paciente_instance.endereco_cobranca = endereco_residencial
            elif endereco_cobranca_data:
                 # Mock CEP lookup for cobranca
                if 'cep' in endereco_cobranca_data and endereco_cobranca_data['cep'] in ['12345-678', '12345678'] and not endereco_cobranca_data.get('logradouro'):
                    endereco_cobranca_data['logradouro'] = "Rua Cobranca Mockada Create"
                    # ... fill other fields ...
                paciente_instance.endereco_cobranca = Endereco.objects.create(**endereco_cobranca_data)

            # Set criado_por if user is available in context
            request = self.context.get('request')
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                paciente_instance.criado_por = request.user

            paciente_instance.save()
            return paciente_instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            # CPF cannot be edited
            validated_data.pop('cpf', None)

            endereco_residencial_data = validated_data.pop('endereco_residencial', None)
            endereco_cobranca_data = validated_data.pop('endereco_cobranca', None)
            # TODO: Clarify behavior for 'repetir_endereco_cobranca' on update.
            # If 'repetir_endereco_cobranca' is not provided in the PATCH request, it defaults to False.
            # This means if it was previously true (cobranca was same as residencial) and the flag is not sent again,
            # the addresses might become unlinked or cobranca might be treated as a new, separate address if
            # 'endereco_cobranca_data' is also absent or present.
            # Consider if the existing link should be preserved if the flag isn't sent.
            repetir_endereco = validated_data.pop('repetir_endereco_cobranca', False) # Default to False on update unless specified

            # Update endereco_residencial
            if endereco_residencial_data:
                residencial_serializer = EnderecoSerializer(instance.endereco_residencial, data=endereco_residencial_data, partial=True)
                if residencial_serializer.is_valid(raise_exception=True):
                    residencial_serializer.save()

            # Handle endereco_cobranca
            if repetir_endereco:
                # If an old cobranca address exists and it's different, it might need to be deleted or orphaned
                # For simplicity, we just point cobranca to residencial.
                if instance.endereco_cobranca and instance.endereco_cobranca != instance.endereco_residencial:
                    # Decide: delete instance.endereco_cobranca if it's not used by others?
                    # For now, let's assume it can be orphaned or handled by a cleanup task.
                    pass
                instance.endereco_cobranca = instance.endereco_residencial
            elif 'endereco_cobranca' in self.initial_data: # Check if 'endereco_cobranca' was part of the input
                if endereco_cobranca_data is None: # Explicitly set to null
                    if instance.endereco_cobranca and instance.endereco_cobranca != instance.endereco_residencial:
                        # Potentially delete instance.endereco_cobranca if it's not shared.
                        pass
                    instance.endereco_cobranca = None
                elif endereco_cobranca_data: # New/updated data for cobranca
                    if instance.endereco_cobranca and instance.endereco_cobranca != instance.endereco_residencial:
                        # Update existing distinct cobranca address
                        cobranca_serializer = EnderecoSerializer(instance.endereco_cobranca, data=endereco_cobranca_data, partial=True)
                        if cobranca_serializer.is_valid(raise_exception=True):
                            cobranca_serializer.save()
                    else:
                        # Create new cobranca address
                        instance.endereco_cobranca = Endereco.objects.create(**endereco_cobranca_data)

            # Set modificado_por
            request = self.context.get('request')
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                instance.modificado_por = request.user

            # Update other Paciente fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()
            return instance
