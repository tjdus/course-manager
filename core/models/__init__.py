from .module import Module
from .permission import Permission
from .role import Role
from .student import Student
from .professor import Professor
from .department import Department
from .course import Course
from .enrollment import Enrollment
from .completed_couse import CompletedCourse
from .semester import Semester

__all__ = ['Student', 'Professor', 'Department', 'Course', 'User', 'UserRole', 'Role', 'Permission', 'Module', 'Enrollment', 'CompletedCourse', 'Semester']

from .user_role import UserRole
from .user import User