from rest_framework import viewsets
from .models import Professional
from .serializers import ProfessionalSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    summary="Cria um novo profissional de saúde",
    description="Cadastra um profissional com nome social, profissão, endereço e contato.",
    examples=[
        OpenApiExample(
            "Exemplo de criação",
            value={
                "name_social": "Dr. Alex Silva",
                "profession": "Psicólogo",
                "address": "Rua A, 123",
                "contact": "alex@exemplo.com",
            },
        )
    ],
)
class ProfessionalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar profissionais de saúde.
    Endpoints:
    - GET /api/professional/ - Lista todos os profissionais
    - POST /api/professional/ - Cria novo profissional
    - GET /api/professional/{id}/ - Detalhe de um profissional
    - PUT /api/professional/{id}/ - Atualiza profissional
    - PATCH /api/professional/{id}/ - Atualiza parcialmente
    - DELETE /api/professional/{id}/ - Remove profissional
    """

    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
