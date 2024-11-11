from rest_framework import serializers
from .models import Enrollment, Student, Course
from .serializers import StudentSerializer, CourseSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    #TODO:
    #student, course는 읽기 전용으로
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    #학생과 강의의 ID를 받아서 Enrollment와 연결
    #queryset=Student.objects.all(), queryset=Course.objects.all()은 유효한 학생과 강의 객체들만 참조할 수 있도록 제한
    student_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Student.objects.all())
    course_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Course.objects.all())

    class Meta:
        model = Enrollment
        fields="__all__"

    def create(self, validated_data):
        student_data = validated_data.pop('student_id')
        course_data = validated_data.pop('course_id')

        # Enrollment 인스턴스 생성
        enrollment = Enrollment.objects.create(student=student_data, course=course_data, **validated_data)
        return enrollment

    def update(self, instance, validated_data):
        student_data = validated_data.pop('student_id', None)
        course_data = validated_data.pop('course_id', None)

        if student_data:
            instance.student = student_data
        if course_data:
            instance.course = course_data

        instance.save()
        return instance