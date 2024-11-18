from .module import Module
from .permission import Permission
from .role import Role
from .student import Student
from .professor import Professor
from .department import Department
from .course import Course
from .enrollment import Enrollment

__all__ = ['Student', 'Professor', 'Department','Enrollment', 'Course', 'User', 'UserRole', 'Role', 'Permission', 'Module']

from .user_role import UserRole
from .user import User