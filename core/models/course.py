from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    department = models.ForeignKey("core.department", on_delete=models.CASCADE)
    professor = models.ForeignKey("core.professor", on_delete=models.CASCADE)
    credit = models.IntegerField(default=3)  # 과목의 학점
    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True)  # 선수 과목 목록

    class Meta:
        db_table = 'course'
        verbose_name = '강의'
