from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'department'
        verbose_name = '학과'