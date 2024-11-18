from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    department = models.ForeignKey("core.department", on_delete=models.CASCADE)
    professor = models.ForeignKey("core.professor", on_delete=models.CASCADE)
    prerequisite = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dependent_courses"
    )
    credit = models.IntegerField(default=3)


    class Meta:
        db_table = 'course'
        verbose_name = '강의'
