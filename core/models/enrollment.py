from django.db import models


class Enrollment(models.Model):
    student = models.ForeignKey('core.Student', on_delete=models.PROTECT)
    course = models.ForeignKey('core.Course', on_delete=models.PROTECT)
    enroll_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'enrollment'
        verbose_name = '수강 신청'
        constraints = [models.UniqueConstraint(
            fields=['student', 'course'],
            name='unique_student_course'
        )]