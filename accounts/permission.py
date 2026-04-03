from rest_framework.permissions import IsAuthenticated
from .models import *

class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if not user or user.is_authenticated:
            return False
        return user.tole == "admin"