from django.db import models

# Таблиці для БД тута

class example(models.Model):
    name = models.CharField(max_length=50)

