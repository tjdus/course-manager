from django.db import models
from django.conf import settings

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('ENROLLED', 'Enrolled'), ('DROPPED', 'Dropped')],
        default='ENROLLED'
    )

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrollment_date']
