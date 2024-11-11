from django.db import models
from core.models.student import Student
from core.models.course import Course
#수강신청 정보 포함하는 모델
class Enrollment(models.Model):
    #TODO:
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    class Meta:
        db_table = 'enrollment'
        verbose_name = '수강 등록'
        #같은 학생이 동일한 과목에 중복 등록되지 않도록 보장
        unique_together = ('student', 'course')