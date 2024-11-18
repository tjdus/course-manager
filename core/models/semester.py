from django.db import models


class Semester(models.Model):
    YEAR_CHOICES = [(r, f"{r}학년도") for r in range(2000, 2101)]
    SEMESTER_CHOICES = [
        ("1", "1학기"),
        ("2", "2학기"),
        ("S", "하계학기"),
        ("W", "동계학기"),
    ]

    year = models.IntegerField(choices=YEAR_CHOICES)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)

    class Meta:
        db_table = "semester"
        verbose_name = "학기"
        unique_together = ("year", "semester")
