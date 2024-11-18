from rest_framework import serializers
from core.models import Enrollment
#from .serializers import EnrollmentSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)  # 학생 이름 추가
    course_name = serializers.CharField(source='course.name', read_only=True)  # 과목 이름 추가

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'course_name', 'enrollment_date', 'status']
