from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    пермишен, который позволяет только автору объекта редактировать его.
    Другим пользователям доступно только чтение.
    """

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
      
        return obj.seller == request.user
