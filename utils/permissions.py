from rest_framework.permissions import BasePermission


def check_permission(permission_class, self, request, obj=None):
    #  !!! permission_class must a tuple !!! such like (a,)
    #  self = Class ViewSet self
    self.permission_classes = permission_class
    if obj is not None:
        self.check_object_permissions(request, obj)
    self.check_permissions(request)


class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and ShopUser.objects.filter(user=request.user)
