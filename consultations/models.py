from django.db import models
from professionals.models import Professional


class Consultation(models.Model):
    datetime = models.DateTimeField()
    professional = models.ForeignKey(
        Professional, on_delete=models.CASCADE, related_name="consultations"
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Consulta {self.id} - {self.professional} @ {self.datetime}"
