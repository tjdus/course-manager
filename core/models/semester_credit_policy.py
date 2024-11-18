from django.db import models


class SemesterCreditPolicy(models.Model):
    semester = models.ForeignKey('core.Semester', on_delete=models.CASCADE)
    max_credits = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        db_table = "semester_credit_policy"
        verbose_name = "학기 학점 정책"
