from rest_framework import serializers

from core.models import Enrollment, Course, Student 
from core.serializers.course import CourseSerializer
from core.serializers.student import StudentSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset =Student.objects.all())
    course_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset= Course.objects.all())
    class Meta:
        model =  Enrollment
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        student_data = validated_data.pop('student_id')
        course_data = validated_data.pop('course_id')

        enrollment = Enrollment.objects.create(student=student_data, course=course_data, **validated_data)
        return enrollment
    
    def update(self, instance, validated_data):
        student_data = validated_data.pop('student_id')
        course_data = validated_data.pop('course_id')

        if student_data:
            instance.student = student_data
        
        if course_data:
            instance.course = course_data

        instance.save()
        return instance

