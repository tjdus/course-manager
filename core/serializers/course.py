from rest_framework import serializers

from core.models import Course, Department, Professor
from core.serializers.department import DepartmentSerializer
from core.serializers.professor import ProfessorSerializer


class CourseSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer(read_only=True)
    # professor = ProfessorSerializer(read_only=True)
    # department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), write_only=True)
    # professor_id = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all(), write_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['id']

