from rest_framework.views import APIView


class EnrollmentListView(APIView):
    #TODO:

    # 수강 신청 조회

    # 수강 신청 생성
    permission_classes = [IsAuthenticated]

    # 수강 신청 목록 조회
    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        course_id = request.data.get('course_id')
        #해당 과목이 존재하지 않는 경우 예외 처리
        #클라이언트가 보낸 course_id를 기반으로 Course 객체를 찾고, 이를 course 변수에 저장
        course = get_object_or_404(Course, id=course_id)
        #이미 존재하는 수강 신청인 경우
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response(
                {"오류": "이미 신청한 과목입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        #학생이 해당 과목을 수강할 수 있는 그룹에 속하지 않은 경우
        if not self.is_student_in_allowed_group(request.user, course):
            return Response(
                {"오류": "수강 가능한 그룹에 속하여 있지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        #학생의 수강 학점 한도가 초과된 경우
        if self.is_credit_limit_exceeded(request.user, course):
            return Response(
                {"오류": "수강 가능 학점을 초과했습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        #학생이 선수 과목을 이수하지 않은 경우
        if not self.has_completed_prerequisites(request.user, course):
            return Response(
                {"오류": "선수 과목을 이수하지 않았습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 모든 조건을 통과한 경우 수강 신청 생성
        enrollment = Enrollment.objects.create(student=request.user, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def is_student_in_allowed_group(self, student, course):
        # 학생의 학과와 과목의 학과가 일치하는지 확인
        #국어국문학과 학생은 국어국문학 수업만 들을 수 있음
        return student.department == course.department

    pass



class EnrollmentDetailView(APIView):
    #TODO:
    permission_classes = [IsAuthenticated]

    # 수강 신청 조회
    def get(self, request, pk):
        # 현재 로그인한 학생의 특정 수강 신청 내역 조회
        #pk와 student가 현재 로그인한 사용자(request.user)와 일치하는 Enrollment 객체를 조회
        enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 수강 신청 삭제
    def delete(self, request, pk):
        # 현재 로그인한 학생의 특정 수강 신청 내역을 삭제
        #pk와 student가 현재 로그인한 사용자(request.user)와 일치하는 Enrollment 객체를 조회
        enrollment = get_object_or_404(Enrollment, pk=pk, student=request.user)

        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    pass