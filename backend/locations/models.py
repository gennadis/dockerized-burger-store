from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class Location(models.Model):
    address = models.CharField(
        verbose_name="адрес",
        max_length=200,
        unique=True,
    )
    latitude = models.DecimalField(
        verbose_name="широта",
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ],
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        verbose_name="долгота",
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ],
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
    )
    requested_at = models.DateTimeField(
        verbose_name="запрос координат осуществлен",
        default=timezone.now,
    )

    class Meta:
        verbose_name = "локация"
        verbose_name_plural = "локации"

    def __str__(self):
        return self.address
