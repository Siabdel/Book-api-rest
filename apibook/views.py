from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

from rest_framework import generics
from apibook import models as api_models
from rest_framework import permissions
from apibook.serializers import BookSerializer
from apibook import serializers as api_json
from apibook.permissions import BasePermissions, IsAuthorOrReadOnly, IsAuthor

# Empty view

def Empty_view(request):
        return render('')

class BookList(generics.ListCreateAPIView):
    queryset = api_models.Book.objects.all()
    serializer_class = api_json.BookSerializer
    

class BookDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = api_models.Book.objects.all()
    serializer_class = api_json.BookSerializer
    permission_classes = (IsAuthorOrReadOnly)

class AuthorList(generics.ListCreateAPIView):
    queryset = api_models.Author.objects.all()
    serializer_class = api_json.AuteurSerializer

class AuthorDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = api_models.Author.objects.all()
    serializer_class = api_json.AuteurSerializer
    
class BlogList(generics.ListCreateAPIView):
    queryset = api_models.Blog.objects.all()
    serializer_class = api_json.BlogSerializer

class BlogDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = api_models.Blog.objects.all()
    serializer_class = api_json.BlogSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
   
