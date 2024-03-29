# -*- coding: utf-8 -*-
"""This file
This program bank of api
"""

__author__ = 'Abdelaziz Sadquaoui'
__copyright__ = 'Copyright (c) 2022 AtlassV'
__version__ = '0.9'

from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey


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
    
class Author(models.Model):
    """
    API Author
    Args:
        models (_type_): _description_
    """
    username  = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname  = models.CharField(max_length=100)
    site_url  = models.URLField(blank=True, null=True)

    class Meta :
        verbose_name = ('Auteur')
        ordering = ('firstname', 'lastname')
    
    def __unicode__(self):
        return u'%s %s' % (self.firstname, self.lastname)

    def __str__(self):
        return u'%s %s' % (self.username, self.lastname)

class Book(models.Model):
    """_summary_
    API books  
    Args:
        models (_type_): _description_
    """
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    authors     = models.ManyToManyField(Author, related_name="mes_auteurs")
    published   = models.DateTimeField(blank=True, null=True)
    created     = models.DateTimeField(auto_now=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    google_link = models.URLField(blank=True, null=False)
    page_count  = models.SmallIntegerField(blank=True, null=True)
    categorie   = models.ManyToManyField(Category)
    image_link  = models.URLField(blank=True, null=False)
    isbn_13     = models.CharField(max_length=13,blank=True, null=True)
    buy_link    = models.URLField(blank=True, null=False)
    
    def __str__(self) -> str:
        return self.title
    

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(Author)
    
    def __str__(self) -> str:
        return self.title

class ParamTimerPrayer(models.Model):
    ville  = models.CharField(max_length=100) 
    pays   = models.CharField(max_length=100) 
    population = models.IntegerField(blank=True, null=True)
    methode  = models.CharField(max_length=100) 
    longitude = models.DecimalField(max_digits=5, decimal_places=3)
    latitude  = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        ordering = ["ville", ]
        unique_together = ["ville", ]
   
    def __str__(self):
        return "{}".format(self.ville)