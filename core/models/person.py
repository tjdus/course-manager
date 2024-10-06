from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True