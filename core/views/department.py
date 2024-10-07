from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Department
from core.serializers.department import DepartmentSerializer


class DepartmentListAPIView(APIView):
    def get_queryset(self):
        return Department.objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = DepartmentSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailAPIView(APIView):
    def get_queryset(self):
        return Department.objects.all()

    def get_object(self, pk):
        qs = self.get_queryset().get(pk=pk)
        return qs

    def get(self, request, pk, *args, **kwargs):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)