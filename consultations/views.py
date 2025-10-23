from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Consultation
from .serializers import ConsultationSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(
    summary="Registra uma nova consulta médica",
    description="Cadastra uma consulta vinculada a um profissional de saúde, com data e hora.",
    examples=[
        OpenApiExample(
            "Exemplo de criação de consulta",
            value={
                "professional": 1,
                "datetime": "2024-07-15T14:30:00Z",
                "notes": "Consulta de rotina para avaliação geral.",
            },
        )
    ],
)
class ConsultationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar consultas.
    Endpoints:
    - GET /api/consultas/ - Lista todas as consultas
    - POST /api/consultas/ - Cria nova consulta
    - GET /api/consultas/{id}/ - Detalhe de uma consulta
    - PUT /api/consultas/{id}/ - Atualiza consulta
    - PATCH /api/consultas/{id}/ - Atualiza parcialmente
    - DELETE /api/consultas/{id}/ - Remove consulta
    """

    queryset = Consultation.objects.select_related("professional").all()
    serializer_class = ConsultationSerializer
    filter_backends = [filters.SearchFilter]

    @action(
        detail=False,
        methods=["get"],
        url_path="professional/(?P<professional_id>[^/.]+)",
        url_name="by_professional",
    )
    def by_professional(self, request, professional_id=None):
        """
        Search consultations by professional ID.
        Endpoint: GET /api/consultations/professional/{professional_id}/
        """
        queryset = self.get_queryset().filter(professional_id=professional_id)

        status_filter = request.query_params.get("status", None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
