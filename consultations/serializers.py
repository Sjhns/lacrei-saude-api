from rest_framework import serializers
from .models import Consultation
from django.utils import timezone


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ["id", "datetime", "professional", "notes"]

    def validate_datetime(self, value):

        if value < timezone.now():
            raise serializers.ValidationError(
                "A data/hora da consulta não pode ser no passado"
            )
        return value
