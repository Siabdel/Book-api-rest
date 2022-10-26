from django.contrib import admin

# Register your models here.
import apibook.models as api_models

#-----------------
# Project
# ---------------
class CategoryAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  api_models.Category._meta.get_fields()]
    list_total.remove('book')
    list_display = list_total


class AuthorAdmin(admin.ModelAdmin) :
    list_total  = [ f.name for f in  api_models.Author._meta.get_fields()]
    list_display = list_total
    list_display = ['id', 'username', 'firstname', 'lastname']
    
class BookAdmin(admin.ModelAdmin):
    list_total  = [ f.name for f in  api_models.Book._meta.get_fields()]
    list_total.remove('authors')
    list_total.remove('categorie')
    list_display = list_total

class BlogAdmin(admin.ModelAdmin):
    list_total  = [ f.name for f in  api_models.Blog._meta.get_fields()]
    #list_total.remove('author')
    
    
admin.site.register(api_models.Author, AuthorAdmin)
admin.site.register(api_models.Category, CategoryAdmin)
admin.site.register(api_models.Book, BookAdmin)
admin.site.register(api_models.Blog, BlogAdmin)
