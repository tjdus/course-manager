from django.db import models

from core.models.person import Person


class Student(Person):
    student_id = models.CharField(max_length=10, verbose_name="학번")
    department = models.ForeignKey("core.department", on_delete=models.PROTECT)
    current_credits = models.IntegerField(default=0)  # 현재 수강 학점
    max_credits = models.IntegerField(default=18)  # 최대 수강 가능 학점
    completed_courses = models.ManyToManyField(Course, related_name="completed_students", blank=True)  # 이수한 과목 목록

    class Meta:
        db_table = 'student'
        verbose_name = '학생'