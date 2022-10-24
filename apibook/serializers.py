from dataclasses import field
from rest_framework import serializers
from apibook import models as api_models

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        fields =  [ f.name for f in  api_models.Book._meta.get_fields()]
        fields.remove('author')
        model  = api_models.Book
        
class AuteurSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = api_models.Author
        
class CategorieSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = api_models.Category
        
        