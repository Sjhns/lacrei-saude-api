from django.db import models


class Professional(models.Model):
    name_social = models.CharField(max_length=255)
    profession = models.CharField(max_length=150)
    address = models.TextField(blank=True)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name_social} — {self.profession}"
