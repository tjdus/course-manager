from django.db import models

from core.models.role import Role
from core.models.user import User


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
