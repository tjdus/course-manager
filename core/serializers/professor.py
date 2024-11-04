from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from core.models import Professor, Department
from core.serializers.department import DepartmentSerializer


class ProfessorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = Professor
        fields = '__all__'

    def create(self, validated_data):
        department_data = validated_data.pop('department')

        try:
            department = Department.objects.get(**department_data)
        except ObjectDoesNotExist:
            raise ValidationError("Department not found with the provided data")

        professor = Professor.objects.create(department=department, **validated_data)
        return professor

    def update(self, instance, validated_data):
        department_data = validated_data.pop('department', None)

        if department_data:
            try:
                department = Department.objects.get(**department_data)
                instance.department = department
            except ObjectDoesNotExist:
                raise ValidationError("Department not found with the provided data")

        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.save()
        return instance
