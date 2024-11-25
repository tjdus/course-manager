# Generated by Django 4.2 on 2024-11-18 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_enrollment'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='enrollment',
            constraint=models.UniqueConstraint(fields=('student', 'course'), name='unique_student_course'),
        ),
    ]