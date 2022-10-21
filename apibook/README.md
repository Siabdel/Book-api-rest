
![projet](images/rest_api_with_django.jpeg)

#  Rest APIs with Django Framework


>  Créer des APIs web avec Django rest framework
>
> Django for APIs est un guide basé sur des projets pour créer des API modernes avec Django & Django REST Framework. Il convient aux débutants qui n'ont jamais construit d'API auparavant ainsi qu'aux programmeurs professionnels à la recherche d'une introduction rapide aux principes fondamentaux et aux meilleures pratiques de Django.



## la configuration initiale

on va commencer par installer notre virtualenv puis ensuite on installe Django.

Créer le project **bookapirest** et l'application **bookapi**

##### Creer un virtualenv 

```shell
$ mkvirtualenv envBookApiRest
$ workon envBookApiRest
$ cdvirtualenv
```

##### installer Django framework 

```shell
$ pip install django
$ pip install djangorestframework
$ django-admin startproject bookapirest
$ cd bookapirest
$ ./manage.py startapp bookapi
```



Il faut ajouter l'application **bookapi** dans la liste **INSTALLED_APPS** se

ttings.py

```python
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd-party apps
    #"rest_framework",  # new
    #"corsheaders",  # new
    # Local
    # "accounts.apps.AccountsConfig",  # new
    "apibook.apps.apibookConfig",  # new
]
```



###### Migarte les models 

```shell
$ ./manage.py migrate 
```



##### Model

Trois  tables dans notre modes.py 

* Category
* Auteur
* Book



###### **Category  :**

```python
# Create your models here.

class Category(models.Model):
    """Category model.
    """
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)
    
    def __unicode__(self):
        return u'%s' % self.title
    def __str__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return ("category_detail", (), {"slug": self.slug})
```



###### **Author :**

```python
class Author(models.Model):
    """
    API Author
    Args:
        models (_type_): _description_
    """

    firstname = models.CharField(max_length=100)
    lastname  = models.CharField(max_length=100)
    site_url  = models.URLField(blank=True, null=True)

    class Meta :
        verbose_name = ('Auteur')
        ordering = ('firstname', 'lastname')
    
    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

    def __str__(self):
        return u'%s %s' % (self.firstname, self.lastname)

```



###### **Book :**



```python
class Book(models.Model):
    """_summary_
    API books  
    Args:
        models (_type_): _description_
    """
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    author      = models.ManyToManyField(Author, related_name="mes_autheurs")
    published   = models.DateTimeField(blank=True, null=True)
    created     = models.DateTimeField(auto_now=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    google_link = models.URLField(blank=True, null=False)
    page_count  = models.SmallIntegerField(blank=True, null=True)
    categorie   = models.ManyToManyField(Category)
    image_link  = models.URLField(blank=True, null=False)
    isbn_13     = models.CharField(max_length=13,blank=True, null=True)
    buy_link    = models.URLField(blank=True, null=False)
    
```



###### Création du super utilisateur 

```shell
$ ./manage.py createsuperuser
```



###### Construire admin manager

```python
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
    
class BookAdmin(admin.ModelAdmin):
    list_total  = [ f.name for f in  api_models.Book._meta.get_fields()]
    list_total.remove('author')
    list_total.remove('categorie')
    list_display = list_total

admin.site.register(api_models.Author, AuthorAdmin)
admin.site.register(api_models.Category, CategoryAdmin)
admin.site.register(api_models.Book, BookAdmin)

```



![ecran dmin](images/Ecran_admin.png)



#### deployament  sur GIT

```shell
$ git init
$ git branch -M main
$ git pull origin main
$ #
$ git commit -am "init project REST API book with Django"
$ git push origin main

```



## Annexes 

CREATE TABLE "appipro_product" ("id" serial NOT NULL PRIMARY KEY, "name" varchar(100) NOT NULL UNIQUE)
$ ./manage.py dumpdata --format json --indent 2 appipro
$ ./manage.py sqlmigrate  appipro 0001_initial >> schema_001.sql
$ ./manage.py dumpdata -table users db/users.json
$ ./manage.py dumpdata -table django-users 
$ ./manage.py dumpdata  django-users 

$ CREATE TABLE "appipro_product" ("id" serial NOT NULL PRIMARY KEY);