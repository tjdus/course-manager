def create_initial_data(apps, schema_editor):
    Module = apps.get_model("your_app_name", "Module")
    Permission = apps.get_model("your_app_name", "Permission")
    Role = apps.get_model("your_app_name", "Role")

    # Lecture Management module and permissions
    lecture_management_module, _ = Module.objects.get_or_create(name="Lecture Management")
    create_lecture, _ = Permission.objects.get_or_create(name="Create Lecture", module=lecture_management_module)
    edit_lecture, _ = Permission.objects.get_or_create(name="Edit Lecture", module=lecture_management_module)
    delete_lecture, _ = Permission.objects.get_or_create(name="Delete Lecture", module=lecture_management_module)

    # Enrollment module and permissions
    enrollment_module, _ = Module.objects.get_or_create(name="Enrollment")
    apply_enrollment, _ = Permission.objects.get_or_create(name="Apply Enrollment", module=enrollment_module)
    cancel_enrollment, _ = Permission.objects.get_or_create(name="Cancel Enrollment", module=enrollment_module)

    # Create roles and assign permissions
    professor_role, _ = Role.objects.get_or_create(name="Professor")
    professor_role.permissions.set([create_lecture, edit_lecture, delete_lecture])

    student_role, _ = Role.objects.get_or_create(name="Student")
    student_role.permissions.set([apply_enrollment, cancel_enrollment])
