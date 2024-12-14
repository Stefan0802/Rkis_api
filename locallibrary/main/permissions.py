from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только администраторам для создания, изменения и удаления книг.
    Остальные пользователи могут только просматривать книги.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff