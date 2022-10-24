from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from apibook import models as api_models
from apibook.serializers import BookSerializer
from apibook import serializers as api_json

class BookList(generics.ListCreateAPIView):
    queryset = api_models.Book.objects.all()
    serializer_class = api_json.BookSerializer
    

class BookDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = api_models.Book.objects.all()
    serializer_class = api_json.BookSerializer
    
class AuthorList(generics.ListCreateAPIView):
    queryset = api_models.Author.objects.all()
    serializer_class = api_json.AuteurSerializer

class AuthorDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = api_models.Author.objects.all()
    serializer_class = api_json.AuteurSerializer
    
