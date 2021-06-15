from django.db import models

# Create your models here.


class CSVModel(models.Model):

    symbol = models.CharField(
        null=True,
        blank=True,
        max_length=60
    )
    date = models.DateField(
        null=True,
        blank=True
    )
    open = models.FloatField(
        null=True,
        blank=True
    )
    high = models.FloatField(
        null=True,
        blank=True
    )
    low = models.FloatField(
        null=True,
        blank=True
    )
    close = models.FloatField(
        null=True,
        blank=True
    )
    volume = models.IntegerField(
        null=True,
        blank=True
    )
    adj_close = models.FloatField(
        null=True,
        blank=True
    )
    created_by = models.IntegerField(
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
