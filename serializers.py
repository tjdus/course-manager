from rest_framework import serializers
from core.models.enrollment import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date']  # 필요 필드를 추가
