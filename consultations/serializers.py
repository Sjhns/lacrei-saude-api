from rest_framework import serializers
from django.utils import timezone
from .models import Consultation
from professionals.models import Professional


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = "__all__"

    def validate_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "A data/hora da consulta não pode ser no passado."
            )
        return value

    def validate_professional(self, value):
        if not Professional.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Profissional informado não existe.")
        return value

    def validate(self, attrs):
        """
        Regras adicionais de negócio:
        - Impedir consultas duplicadas no mesmo horário para o mesmo profissional
        """
        professional = attrs.get("professional")
        datetime_ = attrs.get("datetime")

        if Consultation.objects.filter(
            professional=professional, datetime=datetime_
        ).exists():
            raise serializers.ValidationError(
                "Já existe uma consulta agendada para este horário com o mesmo profissional."
            )
        return attrs
