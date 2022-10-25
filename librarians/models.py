from django.contrib.auth.models import AbstractUser
from django.db import models


class ShiftOptions(models.TextChoices):
    MORNING = "Matutino"
    AFTERNOON = "Vespertino"
    NIGHT = "Noturno"
    DEFAULT = "Não informado"


class Librarian(AbstractUser):
    shift = models.CharField(
        max_length=50,
        choices=ShiftOptions.choices,
        default=ShiftOptions.DEFAULT,
        null=True,
        blank=True,
    )
    ssn = models.PositiveIntegerField(unique=True)
    birthdate = models.DateField()

    REQUIRED_FIELDS = ["ssn", "birthdate"]
