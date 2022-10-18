from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Класс доступа Суперюзера и Админов к управлению контентом проекта.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsModeratorOrAdminOrOwner(permissions.BasePermission):
    """
    Класс, позволяющий Админам и Модераторам
    удалять и редактировать любые отзывы и комментариии,
    a также Авторам отзыва или комментария
    удалять и редактировать собственные отзывы и комментариии.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role in ('admin', 'moderator')
                or obj.author == request.user
            )
        )
