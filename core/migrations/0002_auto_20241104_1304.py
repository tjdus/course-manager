from django.db import migrations

from core.models import Role


def create_initial_data(apps, schema_editor):
    Department = apps.get_model("core", "Department")
    Student = apps.get_model("core", "Student")
    Professor = apps.get_model("core", "Professor")
    Module = apps.get_model("core", "Module")
    Permission = apps.get_model("core", "Permission")
    User = apps.get_model("core", "User")

    computer_science, _ = Department.objects.get_or_create(
        name="컴퓨터공학과",
        description="컴퓨터공학과 학과 설명"
    )

    student_user_1, _ = User.objects.get_or_create(username="student1", password="password123")
    student_user_2, _ = User.objects.get_or_create(username="student2", password="password123")
    professor_user, _ = User.objects.get_or_create(username="professor1", password="password123")

    Student.objects.get_or_create(
        name="Student1",
        email="student1@example.com",
        phone_number="01012345678",
        student_id="202201",
        department=computer_science,
    )

    Student.objects.get_or_create(
        name="Student2",
        email="student2@example.com",
        phone_number="01087654321",
        student_id="202202",
        department=computer_science,
    )

    # Professor 데이터 생성
    Professor.objects.get_or_create(
        name="Professor1",
        email="professor1@example.com",
        phone_number="01011223344",
        employee_id="P001",
        department=computer_science,
    )

    lecture_management_module, _ = Module.objects.get_or_create(name="Lecture Management")

    enrollment_module, _ = Module.objects.get_or_create(name="Enrollment")

    create_lecture, _ = Permission.objects.get_or_create(name="Create Lecture", module=lecture_management_module)
    edit_lecture, _ = Permission.objects.get_or_create(name="Edit Lecture", module=lecture_management_module)
    delete_lecture, _ = Permission.objects.get_or_create(name="Delete Lecture", module=lecture_management_module)

    apply_enrollment, _ = Permission.objects.get_or_create(name="Apply Enrollment", module=enrollment_module)
    cancel_enrollment, _ = Permission.objects.get_or_create(name="Cancel Enrollment", module=enrollment_module)

    # Role 생성 및 Permission 할당
    professor_role, _ = Role.objects.get_or_create(name="Professor")
    professor_role.permissions.set([create_lecture.id, edit_lecture.id, delete_lecture.id])

    student_role, _ = Role.objects.get_or_create(name="Student")
    student_role.permissions.set([apply_enrollment.id, cancel_enrollment.id])

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
