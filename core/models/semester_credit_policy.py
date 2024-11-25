from django.db import models


class SemesterCreditPolicy(models.Model):
    semester = models.ForeignKey('core.Semester', on_delete=models.PROTECT)
    max_credits = models.IntegerField(default=19)

    class Meta:
        db_table = "semester_credit_policy"
        verbose_name = "학기 학점 정책"
