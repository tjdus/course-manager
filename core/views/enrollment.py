from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Enrollment
from core.serializers.enrollment import EnrollmentSerializer

class EnrollmentListView(APIView):
    """
    로그인한 사용자의 모든 수강 신청 목록을 조회하거나 새로운 수강 신청을 생성하는 API
    """
    def get(self, request):
        # 현재 로그인한 사용자의 수강 신청 목록 조회
        enrollments = Enrollment.objects.filter(student=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # 새로운 수강 신청 생성
        data = request.data
        data['student'] = request.user.id  # 로그인한 사용자 정보 추가
        serializer = EnrollmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Enrollment 인스턴스 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDetailView(APIView):
    """
    특정 수강 신청 내역을 조회, 수정 또는 삭제하는 API
    """
    def get_object(self, pk, user):
        # 특정 수강 신청 객체를 가져오고, 현재 사용자와 연관된지 확인
        try:
            enrollment = Enrollment.objects.get(pk=pk, student=user)
            return enrollment
        except Enrollment.DoesNotExist:
            return None

    def get(self, request, pk):
        # 특정 수강 신청 내역 조회
        enrollment = self.get_object(pk, request.user)
        if enrollment is None:
            return Response({"error": "Enrollment not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # 특정 수강 신청 삭제
        enrollment = self.get_object(pk, request.user)
        if enrollment is None:
            return Response({"error": "Enrollment not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)
        enrollment.delete()
        return Response({"message": "Enrollment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
