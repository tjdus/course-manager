from django.db import models


class Enrollment(models.Model):
    student = models.ForeignKey("core.student", on_delete=models.CASCADE)
    course = models.ForeignKey("core.course", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'enrollment'
        verbose_name = '수강조회'