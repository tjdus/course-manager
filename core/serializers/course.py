from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from core.models import Course, Department, Professor
from core.serializers.department import DepartmentSerializer
from core.serializers.professor import ProfessorSerializer


class CourseSerializer(serializers.ModelSerializer):
    #read_only=True : 데이터를 수정할 필요가 없고, 오직 클라이언트에게 보여주기 위해 사용
    #write_only=True: 데이터를 생성/업데이트할 때는 사용, 조회 시에는 표시 X
    department = DepartmentSerializer(read_only=True)
    professor = ProfessorSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Department.objects.all())
    professor_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Professor.objects.all())

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        #department_id와 professor_id는 validated_data에서 꺼내 각각 department_data와 professor_data로 저장
        department_data = validated_data.pop('department_id')
        professor_data = validated_data.pop('professor_id')
        #강의를 생성하면서, 꺼낸 학과와 교수 ID를 department와 professor 필드에 설정하고, 나머지 유효성 검사된 데이터도 함께 설정
        course = Course.objects.create(department=department_data, professor=professor_data, **validated_data)
        return course

    def update(self, instance, validated_data):
        #validated_data에서 department_id와 professor_id를 꺼냄
        #값이 없을 경우 기본값으로 None을 설정
        department_data = validated_data.pop('department_id', None)
        professor_data = validated_data.pop('professor_id', None)
        #학과 또는 교수 ID가 주어진 경우
        #instance의 department 또는 professor 필드를 해당 값으로 업데이트
        if department_data:
            instance.department = department_data

        if professor_data:
            instance.professor = professor_data
        #제공된 데이터에 course_name이 있으면 그 값으로 업데이트하고, 없으면 기존 값을 유지
        instance.course_name = validated_data.get('course_name', instance.course_name)
        instance.save()
        return instance


