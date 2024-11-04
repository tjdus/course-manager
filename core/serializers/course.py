from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from core.models import Course, Department, Professor
from core.serializers.department import DepartmentSerializer
from core.serializers.professor import ProfessorSerializer


class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    professor = ProfessorSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Department.objects.all())
    professor_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Professor.objects.all())

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        department_data = validated_data.pop('department_id')
        professor_data = validated_data.pop('professor_id')

        course = Course.objects.create(department=department_data, professor=professor_data, **validated_data)
        return course

    def update(self, instance, validated_data):
        department_data = validated_data.pop('department_id', None)
        professor_data = validated_data.pop('professor_id', None)

        if department_data:
            instance.department = department_data

        if professor_data:
            instance.professor = professor_data

        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.save()
        return instance


