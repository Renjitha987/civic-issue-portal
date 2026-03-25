from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')

class IsWardMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'WARD_MEMBER')

class IsCitizen(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'CITIZEN')

class IsDepartmentHead(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'DEPARTMENT_HEAD')

class BlockedUsersCannotAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        return not request.user.is_blocked
