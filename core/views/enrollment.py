from django.db import transaction, IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Student, Course
from core.models.enrollment import Enrollment
from core.serializers.enrollment import EnrollmentSerializer, EnrollmentRequestSerializer


class EnrollmentListView(APIView):
    def get_queryset(self):
        return Enrollment.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        student = Student.objects.get(user=user)
        qs = self.get_queryset().filter(student=student)
        serializer = EnrollmentSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EnrollmentRequestSerializer,
        responses={
            201: EnrollmentSerializer,
            400: "Bad Request",
            404: "Not Found",
        }
    )
    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            user = request.user
            student = Student.objects.get(user=user)
            serializer = EnrollmentRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            course_id = serializer.validated_data['course_id']
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({"error": "Course not found."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                enrollment = Enrollment.objects.create(course=course, student=student)
            except IntegrityError:
                return Response({"error": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)




class EnrollmentDetailView(APIView):

    def get_queryset(self):
        return Enrollment.objects.all()

    def get_object(self, pk):
        qs = self.get_queryset().get(pk=pk)
        return qs

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        student = Student.objects.get(user=user)
        enrollment = self.get_object(pk)

        if enrollment.student != student:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        student = Student.objects.get(user=user)
        enrollment = self.get_object(pk)
        if enrollment.student != student:
            return Response(status=status.HTTP_404_NOT_FOUND)

        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)