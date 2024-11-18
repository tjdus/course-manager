from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

from core.models.course import Course
from core.models.enrollment import Enrollment
from core.serializers.enrollment import EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated


class EnrollmentListView(APIView):
    #인증된 사용자만 사용가능

    permission_classes = [IsAuthenticated] 
    # 수강 신청 조회
    # 현재 로그인한 학생

    def get_queryset(self):
        queryset = Enrollment.objects.select_related("student", "course").all()
        return queryset

    def get(self, request):
        #로그인한 사용자의 것만
        qs = self.get_queryset().filter(student=request.user)
        serializer = EnrollmentSerializer(qs)
        return Response(serializer.data)
    
    # 수강 신청 생성
    # 로그인한 학생과 받은 course id로 수강신청
    # 존재하거나 이미 한 건 안 됨
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 인증 확인
            return Response(status=401)
        course_id = request.data.get('course_id') 
        #course 자체가 존재하지 않는 경우
        if not Course.objects.filter(id=course_id).exists():
                return Response(
                    {"detail": "Invalid course_id. Course does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        existing_enrollment = Enrollment.objects.filter(
            student=request.user,
            course_id = course_id,
        ).exists()

        #이미 존재하는 수강신청
        if existing_enrollment:
            return Response(
                {"detail": "Enrollment already exists."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class EnrollmentDetailView(APIView):

    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        queryset = Enrollment.objects.select_related("student", "course").all()
        return queryset
    # 수강 신청 조회 

    def get_object(self, pk):
        try:
            enrollment = Enrollment.objects.select_related("student", "course").get(pk=pk)
            if enrollment.student != self.request.user:
                raise Http404("You do not have permission to view this enrollment.")
            
        except Enrollment.DoesNotExist:
        # 객체가 없을 경우 404 에러
            raise Http404("Enrollment not found")

    def get(self, request, pk):
        enrollment = self.get_object(pk)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)
        

    # 수강 신청 삭제 
    def delete(self, request, pk):
        # pk를 사용해 객체를 가져옴
        enrollment = self.get_object(pk)
        enrollment.delete()
        return Response(
            {"detail": "Enrollment deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
    )