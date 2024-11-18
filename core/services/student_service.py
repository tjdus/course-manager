from core.models import CompletedCourse, Semester, Enrollment
from core.models.semester_credit_policy import SemesterCreditPolicy


class StudentEnrollmentService:
    @staticmethod
    def calculate_previous_gpa(student, previous_semester):
        completed_courses = CompletedCourse.objects.filter(student=student, semester=previous_semester)
        if not completed_courses.exists():
            return 0

        gpa_sum = 0
        credit_sum = 0
        for course in completed_courses:
            grade_value = dict(CompletedCourse.GRADE_CHOICES).get(course.grade).split(":")[0]
            gpa_sum += float(grade_value) * course.course.credit
            credit_sum += course.course.credit

        return gpa_sum / credit_sum if credit_sum > 0 else 0.0

    @staticmethod
    def calculate_credits(student, semester):
        enrolled_course = Enrollment.objects.filter(student=student, semester=semester)
        if not enrolled_course.exists():
            return 0

        credit_sum = 0
        for course in enrolled_course:
            credit_sum += course.course.credit
        return credit_sum

    @staticmethod
    def get_max_credits_for_semester(student, semester, gpa):
        try:
            policy = SemesterCreditPolicy.objects.get(semester=semester)
            return policy.max_credits
        except SemesterCreditPolicy.DoesNotExist:
            raise ValueError("No credit policy found for this semester.")

    @staticmethod
    def calculate_credit_limit(student, semester):
        previous_semester = Semester.objects.filter(id__lt=semester.id).order_by('-id').first()
        if not previous_semester:
            return 6

        gpa = StudentEnrollmentService.calculate_previous_gpa(student, previous_semester)

        max_credits = StudentEnrollmentService.get_max_credits_for_semester(student, semester, gpa)

        return max_credits
