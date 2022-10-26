from django.http import request 
from rest_framework import permissions

class BasePermissions(object):
    
    def has_object_permission(self, request, view, obj):
        """ 
        voir si l'user est auteur de l'objet
        """    
        return True
    
    def has_user_permission(self, request, obj):
        """_summary_

        Args:
            request (_type_): _description_
            obj (_type_): _description_
        """
        return True
    

class IsAuthorOrReadOnly(BasePermissions):
    """_summary_

    Args:
        BasePermissions (_type_): _description_
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        for auteur in obj.authors.all():
            if auteur.username == request.user:
                return True
        return False
    

    def has_permission(self, request, obj):
        return True

    