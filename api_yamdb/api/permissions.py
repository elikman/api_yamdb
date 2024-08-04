from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только администраторам.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь право на доступ к представлению.

        Возвращает True, если пользователь аутентифицирован и является
        администратором (is_staff или is_admin).
        """
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее администраторам полный доступ,
    а остальным пользователям - только доступ на чтение.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь право на доступ к представлению.

        Возвращает True, если метод запроса является безопасным
        (например, GET, HEAD, OPTIONS),
        или если пользователь аутентифицирован и является администратором.
        """
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее авторам редактировать свои произведения,
    а остальным пользователям - только доступ на чтение.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, имеет ли пользователь право на доступ к конкретному объекту.

        Возвращает True, если метод запроса является безопасным,
        или если пользователь аутентифицирован и является автором объекта,
        модератором или администратором.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user == obj.author or request.user.is_moderator
                 or request.user.is_admin)
        )
