from core.models import Course
import django_filters

class CourseFilter(django_filters.FilterSet):
    course_name = django_filters.CharFilter(lookup_expr='icontains')
    department_name = django_filters.CharFilter(field_name='department__name', lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['course_name', 'department_name']