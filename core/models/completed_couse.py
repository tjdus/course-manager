from django.db import models


class CompletedCourse(models.Model):
    GRADE_CHOICES = [
        ("A+", "4.3: A+"),
        ("A", "4.0: A"),
        ("A-", "3.7: A-"),
        ("B+", "3.3: B+"),
        ("B", "3.0: B"),
        ("B-", "2.7: B-"),
        ("C+", "2.3: C+"),
        ("C", "2.0: C"),
        ("C-", "1.7: C-"),
        ("D+", "1.3: D+"),
        ("D", "1.0: D"),
        ("F", "0.0: F"),
    ]

    student = models.ForeignKey('core.Student', on_delete=models.PROTECT)
    course = models.ForeignKey('core.Course', on_delete=models.PROTECT)
    semester = models.ForeignKey('core.Semester', on_delete=models.PROTECT)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)

    class Meta:
        db_table = 'completed_course'
        verbose_name = '이수 과목'
