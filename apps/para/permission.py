from rest_framework import permissions

class IsCurrentUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.pemilik == request.user
