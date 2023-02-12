from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin
            )
        )


class IsAdminModeratOrAuthorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )


class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous
