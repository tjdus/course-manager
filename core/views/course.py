from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from core.common.decorators import has_permission
from core.filtersets.course_filter import CourseFilter
from core.models import Course
from core.serializers.course import CourseSerializer


class CourseListAPIView(APIView):
    filterset_class = CourseFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['course_name']

    ordering_fields = ['id', 'course_name']

    def get_queryset(self):
        queryset = Course.objects.select_related("department", "professor").all()
        return queryset

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.
        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request):
        qs = self.filter_queryset(self.get_queryset())
        serializer = CourseSerializer(qs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: "Bad Request"
        },
    )
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
