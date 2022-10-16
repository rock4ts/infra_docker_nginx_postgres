from rest_framework import permissions


class Anonimus(permissions.BasePermission):
    """
    Аноним.
    Может просматривать описания произведений читать отзывы и комментарии.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsRoleUser(permissions.BasePermission):
    """
    Аутентифицированный пользователь.
    Может читать всё, как и Аноним, может публиковать отзывы и ставить оценки
    произведениям (фильмам/книгам/песенкам), может комментировать отзывы;
    может редактировать и удалять свои отзывы и комментарии, редактировать
    свои оценки произведений. Эта роль присваивается по умолчанию каждому
    новому пользователю.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'user'
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )


class IsRoleModeratod(permissions.BasePermission):
    """
    Модератор.
    Те же права, что и у Аутентифицированного пользователя,
    плюс право удалять и редактировать любые отзывы и комментарии.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )


class IsRoleAdmin(permissions.BasePermission):
    """"
    Администратор.
    Полные права на управление всем контентом проекта.
    Может создавать и удалять произведения, категории и жанры.
    Может назначать роли пользователям.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsRoleAdminOrSuperuser(permissions.BasePermission):
    """
    Суперюзер Django.
    Обладает правами администратора, пользователя с правами admin.
    Даже если изменить пользовательскую роль суперюзера — это не лишит
    его прав администратора.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )
