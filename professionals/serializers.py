from rest_framework import serializers
from .models import Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = "__all__"

    def validate_name_social(self, value):
        if not value.strip():
            raise serializers.ValidationError("O nome social é obrigatório.")
        if len(value) < 3:
            raise serializers.ValidationError("O nome social deve ter pelo menos 3 caracteres.")
        return value

    def validate_profession(self, value):
        if not value.strip():
            raise serializers.ValidationError("A profissão é obrigatória.")
        return value
