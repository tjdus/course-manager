"""
URL configuration for course_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core.views.course import CourseListAPIView, CourseDetailAPIView
from core.views.department import DepartmentListAPIView, DepartmentDetailAPIView
from core.views.login import LoginView
from core.views.professor import ProfessorListAPIView, ProfessorDetailAPIView
from core.views.signup import StudentSignupView, ProfessorSignupView
from core.views.student import StudentListView, StudentDetailView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/student/', StudentSignupView.as_view(), name='student_signup'),
    path('signup/professor/', ProfessorSignupView.as_view(), name='professor_signup'),
    path('login/', LoginView.as_view(), name='login'),

    path('course', CourseListAPIView.as_view(), name='course'),
    path('course/<int:pk>/', CourseDetailAPIView.as_view(), name='course'),

    path('department', DepartmentListAPIView.as_view(), name='department'),

    path('department/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department'),

    path('professor', ProfessorListAPIView.as_view(), name='professor'),
    path('professor/<int:pk>', ProfessorDetailAPIView.as_view(), name='professor'),

    path('student', StudentListView.as_view(), name='student'),
    path('student/<int:pk>', StudentDetailView.as_view(), name='student'),
]
