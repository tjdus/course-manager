from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from core.models import Student, Department
from core.serializers.department import DepartmentSerializer


class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Student
        fields = ['id', 'student_id', 'department']

    def create(self, validated_data):
        department_data = validated_data.pop('department')

        try:
            department = Department.objects.get(**department_data)
        except ObjectDoesNotExist:
            raise ValidationError("Department not found with the provided data")

        student = Student.objects.create(department=department, **validated_data)
        return student

    def update(self, instance, validated_data):
        department_data = validated_data.pop('department', None)

        if department_data:
            try:
                department = Department.objects.get(**department_data)
                instance.department = department
            except ObjectDoesNotExist:
                raise ValidationError("Department not found with the provided data")

        instance.student_id = validated_data.get('student_id', instance.student_id)
        instance.save()
        return instance
