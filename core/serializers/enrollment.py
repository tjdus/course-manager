
from rest_framework import serializers
from core.models.enrollment import Enrollment

class EnrollmentRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

"""


from rest_framework import serializers
from core.models.enrollment import Enrollment

class EnrollmentRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()  # course_id 필드 추가

    def validate_course_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid course ID")
        return value

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date']
    """

