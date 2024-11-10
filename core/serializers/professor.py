from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from core.models import Professor, Department
from core.serializers.department import DepartmentSerializer


class ProfessorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Department.objects.all())
    class Meta:
        model = Professor
        fields = '__all__'

    def create(self, validated_data):
        department_data = validated_data.pop('department_id')
        professor = Professor.objects.create(department=department_data, **validated_data)
        return professor

    def update(self, instance, validated_data):
        department_data = validated_data.pop('department_id')

        if department_data:
            instance.department = department_data

        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.save()
        return instance
