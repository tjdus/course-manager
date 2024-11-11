from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from core.models import Student, Department
from core.serializers.department import DepartmentSerializer


class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Student
        fields = "__all__"

    def create(self, validated_data):
        #유효성 검사된 데이터(validated_data)에서 department 데이터를 추출
        department_data = validated_data.pop('department')

        try: #department_data를 기반으로 기존 Department 인스턴스를 조회
            department = Department.objects.get(**department_data)
        except ObjectDoesNotExist: #에러 처리
            raise ValidationError("Department not found with the provided data")
        #유효한 department와 validated_data를 사용하여 Student 객체를 생성하고 반환
        student = Student.objects.create(department=department, **validated_data)
        return student

    def update(self, instance, validated_data):
        #업데이트 요청에서 department 데이터를 추출
        department_data = validated_data.pop('department', None)
        #department_data가 제공되었다면
        if department_data:
            try:# 기존 학과 정보를 조회해 instance.department에 새 학과를 할당
                department = Department.objects.get(**department_data)
                instance.department = department
            except ObjectDoesNotExist: #학과가 없으면 예외처리
                raise ValidationError("Department not found with the provided data")
        #student_id가 제공되면 업데이트하고, 제공되지 않으면 기존 값을 유지
        instance.student_id = validated_data.get('student_id', instance.student_id)
        #인스턴스를 저장하고 업데이트된 인스턴스를 반환
        instance.save()
        return instance
