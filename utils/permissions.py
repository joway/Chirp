from rest_framework.permissions import BasePermission

from users.models import Oauth


def check_permission(permission_class, self, request, obj=None):
    #  !!! permission_class must a tuple !!! such like (a,)
    #  self = Class ViewSet self
    self.permission_classes = permission_class
    if obj is not None:
        self.check_object_permissions(request, obj)
    self.check_permissions(request)


class IsBound(BasePermission):
    def has_permission(self, request, view):
        return Oauth.objects.filter(access_token=request.POST['access_token'])
