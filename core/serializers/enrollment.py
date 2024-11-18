from rest_framework import serializers

from core.models.enrollment import Enrollment
from core.serializers.course import CourseSerializer
from core.serializers.student import StudentSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'student']


class EnrollmentRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(required=True)