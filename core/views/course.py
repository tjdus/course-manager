from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.common.decorators import has_permission
from core.models import Course
from core.serializers.course import CourseSerializer


class CourseListAPIView(APIView):
    def get_queryset(self):
        queryset = Course.objects.select_related("department", "professor").all()
        return queryset
    def get(self, request):
        qs = self.get_queryset()
        serializer = CourseSerializer(qs, many=True)
        return Response(serializer.data)

    @has_permission('Create Lecture')
    def post(self, request, *args, **kwargs):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailAPIView(APIView):
    def get_queryset(self):
        queryset = Course.objects.select_related("department", "professor").all()
        return queryset

    def get_object(self, pk):
        try:
            obj = self.get_queryset().get(pk=pk)
            return obj
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = CourseSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = CourseSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
