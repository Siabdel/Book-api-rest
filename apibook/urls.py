from django.urls import path
from apibook import models as api_models
from apibook import views as api_views

urlpatterns = [
    ## API's endpoints Books
    path("books/", api_views.BookList.as_view(), name="post_list"),
    path("books/<int:pk>/", api_views.BookDetails.as_view(), name="post_detail"),
    path("authors/", api_views.AuthorList.as_view(), name="author_list"),
    path("authors/<int:pk>/", api_views.AuthorDetails.as_view(), name="author_list"),
    ## timedates tools dates dispos , date dans nb jours
    path("dispos/<str:d_start>/", api_views.JsonDataSelect.as_view(),  name="calendar_slot"),
    path("tpass/<int:nbjours>/", api_views.TempsQuiPass.as_view(),  name="temps_qui_pass"),
    ## blogs
    path("blogs/", api_views.BlogList.as_view(), name="blog_list"),
    path("blogs/<int:pk>/", api_views.BlogDetails.as_view(), name="blog_details"),
    ## API time Prayers & Geocoding
    path("geocod/<str:city>/", api_views.GeoCoding.as_view(),  name="geocod_city"),
    path("prayer_time/", api_views.CalendarPrayer.as_view(),  name="prayer_time"),
    path("save_param/", api_views.ParamTimePrayer.as_view(),  name="save_param"),
]