# -*- coding:UTF-8 -*-
from __future__ import unicode_literals
import os, sys
import datetime
import pytz
import json
import io
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.http import Http404
from rest_framework.views import APIView
import numpy as np
import pandas as pd
from dateutil.rrule import advance_iterator, rrule, DAILY
import csv


# Create your views here.

from django.views.generic import ListView
from django.http import JsonResponse
from rest_framework import generics
from apibook import models as api_models
from rest_framework import permissions
from apibook.serializers import BookSerializer
from apibook import serializers as api_json
from apibook.permissions import BasePermissions, IsAuthorOrReadOnly, IsAuthor

# Empty view

def Empty_view(request):
        return render('')


class JsonResponseMixin(object):
    """
    Return json
    """
    def render_to_json(self, queryset):
        # queryset  serialise
        data = serializers.serialize('json', queryset)
        json_data = json.loads( data)
        # json_data = json.dumps( data)
        data_light = [ (elem['pk'], elem['fields']) for elem in json_data ]
        data_light = [ ]
        for elem in json_data:
            elem['fields']['pk'] = elem['pk']
            data_light.append(elem['fields'])

        data_fin = json.dumps(data_light)
        return HttpResponse(data_fin ,  content_type='application/json')

    def queryset_to_json(self, queryset):
        # queryset  serialise
        data = serializers.serialize('json', queryset)

        json_data = json.loads( data)
        # json_data = json.dumps( data)

        # data_light = [ (elem['pk'], elem['fields']) for elem in json_data ]
        data_light = [ ]
        for elem in json_data:
            elem['fields']['pk'] = elem['pk']
            data_light.append(elem['fields'])

        return json.dumps(data_light)

    def dict_to_json(self, data):
        # queryset  serialise
        js_data = json.dumps( data)
        json_data = json.loads(js_data)
        data_light = [ elem  for elem in json_data ]
        return json.dumps(data_light)

    def export_as_json(self,  queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json",  queryset, stream=response)
        return response

    def export_as_cvs(self, queryset):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export_da_{}.csv'.format(queryset.first().pk)
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        # response['Content-Disposition'] = 'attachment; filename="%s"'% os.path.join('export', 'export_of.csv')
        writer = csv.writer(response)
        # les colonnes
        nom_class = queryset.first().__class__
        # ecrire entete du fichier avec les libelles
        all_columns =  all_columns_panda(queryset)
        # writer.writerow(all_columns)


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

 
def genere_datatimes(request):
    # pd.date_range(start='11/11/2022', periods=8)
    # pd.date_range(start='1/1/2018', periods=5, freq='M')
    # pd.date_range(start='1/1/2018', periods=5, freq='3M')
    # tout les heures
    # pd.date_range(start='1/1/2018T13:30', periods=5, freq="1H",  tz='Europe/Paris')
    # tout les 30 mn
    # pd.date_range(start='1/1/2018T13:30', periods=5, freq="15T",  tz='Europe/Paris')

    start = np.datetime64('2022-11-10')
    end = np.datetime64('2023-03-01')
    limit = 100
    delta = np.arange(start,end)
    indices = np.random.choice(len(delta), limit)
    dates_dispos = delta[indices]
    
    return dates_dispos

def generate_slots(requets):
    # pd.timedelta_range(start='1 day', periods=4, closed='right')
    # pd.timedelta_range(start='1 day', end='2 days', freq='6H')
    # tout les heures
    # pd.date_range(start='1/1/2018T13:30', periods=5, freq="1H",  tz='Europe/Paris')
    # tout les 30 mn
    # ['2022-10-11 12:30:00+02:00', '2022-10-11 12:45:00+02:00',
    # '2022-10-11 13:00:00+02:00', '2022-10-11 13:15:00+02:00'
    h_dispos = pd.date_range(start='1/1/2018T13:30', periods=5, freq="15T",  tz='Europe/Paris')
    #
    return h_dispos



class JsonDataSelect(APIView):
    permission_classes = [IsAuthorOrReadOnly, ]
    
    def get_object(self, d_start):
        if not d_start :
          d_start='25/11/2022T08:00'
        dd = "{}/{}/{}T08:00".format(d_start[-2:], d_start[4:6], d_start[:4])
        print(dd) 
        return  dd

    
    def get(self, request, d_start='11/11/2022T08:00', format='json'):
        """_summary_

        Args:
            request (_type_): _description_
            start : date start
            end : end date

        Returns:
            _json: json slots data 
        """
        f_start = self.get_object(d_start)
        # traitement
        slots = []
        bloc_jours = []
        jours_dispos = pd.date_range(start=f_start, periods=10)
        h_dispos = pd.date_range(start=f_start, periods=5, freq="15T",  tz='Europe/Paris')
        
        for jour in jours_dispos:
            blocs = { 'date' : jour, 'slots' : slots}
            for elem in h_dispos :
                slots.append(
                    { "date": elem }
                )
            # add bloc 
            bloc_jours.append({ 'date' : jour, 'slots' : slots})
            slots = []
        # 
        #start   = kwargs.get('start')
        #end   = kwargs.get('end')
        return JsonResponse(bloc_jours, status=200, safe=False)
    
        
        
    
    
    
    