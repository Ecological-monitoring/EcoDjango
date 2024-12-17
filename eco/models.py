from django.db import models

# Таблиці для БД тута

class example(models.Model):
    name = models.CharField(max_length=50)


class Pollutant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class PollutionRecord(models.Model):
    object_name = models.CharField(max_length=100)
    pollutant = models.CharField(max_length=100)
    volume = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.object_name} - {self.pollutant}"
