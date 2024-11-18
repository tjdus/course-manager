from django.db.models import Max
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Student, CompletedCourse


class GPAView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        student = Student.objects.get(user=user)
        completed_courses = CompletedCourse.objects.filter(student=student)

        if not completed_courses.exists():
            return Response({"error": "No completed courses found for this student."}, status=404)

        unique_courses = (
            completed_courses
            .values('course')  # 과목별 그룹화
            .annotate(max_grade=Max('grade'))  # 최고 성적 추출
            .values_list('course', 'max_grade')  # 필요한 필드만 선택
        )

        total_points = 0.0
        total_courses = 0

        for course_id, grade in unique_courses:
            gpa_value = dict(CompletedCourse.GRADE_CHOICES).get(grade, None)
            if gpa_value:
                total_points += float(gpa_value.split(":")[0])
                total_courses += 1

        if total_courses == 0:
            return Response({"error": "No valid grades found for GPA calculation."}, status=400)

        gpa = total_points / total_courses

        return Response({
            "gpa": round(gpa, 2),
            "total_courses": total_courses
        })

