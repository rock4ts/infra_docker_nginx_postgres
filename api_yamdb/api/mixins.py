'''Custom viewset mixins'''
from rest_framework import viewsets

from api_yamdb.settings import admin_methods, moderator_methods
from .permissions import IsAdminOrSuperUser, IsModeratorOrAdminOrOwner


class AdminViewMixin(viewsets.GenericViewSet):
    '''
    Generic viewset class that sets Admin level restrictions for
    'POST', 'PATCH', 'PUT' and 'DELETE' methods.
    '''

    restricted_methods = admin_methods
    permission_level_class = IsAdminOrSuperUser

    def get_permissions(self):
        if self.request.method in self.restricted_methods:
            self.permission_classes = (self.permission_level_class,)
        return super(AdminViewMixin, self).get_permissions()


class ModeratorViewMixin(AdminViewMixin):
    '''
    Generic viewset class that sets Moderator level restrictions for
    'PATCH', 'PUT' and 'DELETE' methods.
    '''

    restricted_methods = moderator_methods
    permission_level_class = IsModeratorOrAdminOrOwner
