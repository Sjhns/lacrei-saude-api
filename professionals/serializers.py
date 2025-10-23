from rest_framework import serializers
from .models import Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ["id", "name_social", "profession", "address", "contact"]

    def validate_name_social(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("name_social não pode ficar vazio")
        return value
