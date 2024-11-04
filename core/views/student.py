from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Student
from core.serializers.student import StudentSerializer


class StudentListView(APIView):
    def get_queryset(self):
        return Student.objects.select_related("department").all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    def get_queryset(self):
        return Student.objects.select_related("department").all()

    def get_object(self, pk):
        student = self.get_queryset().get(pk=pk)
        return student

    def get(self, request, pk, *args, **kwargs):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        student = self.get_object(pk)
        student.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


