from django.db import models


class Record(models.Model):
    city = models.CharField(max_length=255)
    temperature = models.CharField(max_length=255)
    pressure = models.CharField(max_length=255)
    humidity = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.city
