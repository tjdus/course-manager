from django.db import models

from core.models.person import Person


class Professor(Person):
    employee_id = models.CharField(max_length=10)
    department = models.ForeignKey("core.department", on_delete=models.PROTECT)

    class Meta:
        db_table = 'professor'
        verbose_name = '교직원'
