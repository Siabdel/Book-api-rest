from django.http import request 

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
    
    