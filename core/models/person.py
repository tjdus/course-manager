from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    user = models.OneToOneField('core.User', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        abstract = True