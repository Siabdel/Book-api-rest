from django.urls import path
from apibook import models as api_models
from apibook import views as api_views

urlpatterns = [
    path("books", api_views.BookList.as_view(), name="post_list"),
    path("books/<int:pk>/", api_views.BookDetails.as_view(), name="post_detail"),
    path("authors", api_views.AuthorList.as_view(), name="author_list"),
    path("authors/<int:pk>/", api_views.AuthorDetails.as_view(), name="author_list"),

]