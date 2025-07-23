from rest_framework import permissions


class IsOwnerOrReadOnlyPublic(permissions.BasePermission):
    """
    Разрешить владельцу объекта делать всё,
    а всем остальным — только читать публичные привычки.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем всем читать (GET, HEAD, OPTIONS), если привычка публичная
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or obj.user == request.user

        # Для других методов — разрешаем только владельцу
        return obj.user == request.user
