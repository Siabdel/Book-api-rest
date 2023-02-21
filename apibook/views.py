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
from datetime import datetime, timedelta
import requests
import shutil
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

from django.views.generic import ListView
from django.http import JsonResponse
from rest_framework import generics
from apibook import models as api_models
from rest_framework import permissions
from apibook.serializers import BookSerializer
from apibook import serializers as api_json
from apibook.permissions import BasePermissions, IsAuthorOrReadOnly, IsAuthor
from rest_framework.permissions import IsAuthenticated, AllowAny  # NOQA
 
# Empty view

def Empty_view(request):
        return render('')

## dict to object.
class Dictate(object):
    """Object view of a dict, updating the passed in dict when values are set
    or deleted. "Dictate" the contents of a dict...: 
    """
    def __init__(self, dd):
        # since __setattr__ is overridden, self.__dict = d doesn't work
        object.__setattr__(self, '_Dictate__dict', dd)

    # Dictionary-like access / updates
    def __getitem__(self, name):
        value = self.__dict[name]
        if isinstance(value, dict):  # recursively view sub-dicts as objects
            value = Dictate(value)
        return value

    def __setitem__(self, name, value):
        self.__dict[name] = value
    def __delitem__(self, name):
        del self.__dict[name]

    # Object-like access / updates
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value
    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.__dict)
    def __str__(self):
        return str(self.__dict)




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
        # if not d_start :
        # d_start='25/11/2022T08:00'
        dd = "{}/{}/{}T08:00".format(d_start[-2:], d_start[4:6], d_start[:4])
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
        # Serializing json
        # json_object = json.dumps(bloc_jours, indent=4)
        djson = pd.DataFrame(bloc_jours)
        json_object = djson.to_json(orient='records')
        
        with open("/home/django/Depots/www/Vuejs/SPA/service_dom/data2.json", "w") as fd:
            fd.write(json_object)
        return JsonResponse(bloc_jours, status=200, safe=False)
    
class TempsQuiPass(APIView):
    permission_classes = [IsAuthorOrReadOnly, ]
    
    def get(self, requets, nbjours=1):
        # Timedelta function demonstration
        # Using current time
        ini_time_for_now = datetime.now()
        
        # Calculating past dates for nb days
        past_date_before_nbjour = ini_time_for_now + \
                            timedelta(days = nbjours)
        
        # printing calculated past_dates
        #print('past_date_before:', str(past_date_before_nbjour.strftime(%d/%m/%Y)))
        # return 

        date_after_nbjour = past_date_before_nbjour.strftime("%d/%m/%Y")
        data = {
                "nbjours": nbjours,
                "date_start":str(ini_time_for_now),
                "end_date":date_after_nbjour,
            }
        print(data)
        json_data = json.dumps( data)
         
        #
        return JsonResponse(data, status=200, safe=False)
            
class RandomImage(APIView):
    """_summary_

    Args:
        APIView (_type_): _description_
    """
    def get(self, request):
        category = 'nature'
        api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'\
            .format(category)
        response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY', 'Accept': 'image/jpg'}, stream=True)
        if response.status_code == requests.codes.ok:
            with open('img.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        else:
            print("Error:", response.status_code, response.text)

class ToastUiCalendar(APIView):
    """_summary_

    Args:
        APIView (_type_): _description_

    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthorOrReadOnly, ]
    
    def get(self, request, **coordonnees):
         # Using current time
        ini_time_for_now = datetime.now()
        data = {
            'country':'France',
            'city':'Lyon',
            'latitude':45.7578137, 
            "longitude": 4.8320114,
            'method':12,
            'month':2,
            'year':2023,
        }
        ##Example Request: http://api.aladhan.com/v1/calendar?latitude=51.508515&longitude=-0.1254872&method=2&month=4&year=2017
        api_url = 'http://api.aladhan.com/v1/calendar?latitude={latitude}&longitude={longitude}&method={method}&month={month}&year={year}'\
            .format(**data)
        
        print("API url=", api_url) 
        ## construire struct 
        data_schedules = [
            {
              "id": "1",
              "title": "Test ok my schedule from DRF",
              "category": "time",
              "start": "2023-02-09T12:30:00+09:00",
              "end": "2023-02-09T14:30:00+09:00",
              "isPending": False,
              "raw": { "id": "111", "whatisit": "raw option contains user datas" },
              "customStyle": "scheduleTeste",
              "bgColor": "red",
              "color": "white",
              "body": "body texte",
              "location": "home/garden",
              "attendees": ["User A", "User B"],
            },
            {
              "id": "2",
              "title": "my schedule 2 From DRF *",
              "category": "time",
              "start": "2023-02-09T12:30:00+09:00",
              "end": "2023-02-09T13:30:00+09:00",
              "bgColor": "red",
              "dragBgColor": "red",
              "borderColor": "black",
              "color": "white",
            },
            ]
        #today = datetime.utcnow()
        #today = datetime.now(tz=pytz.UTC)
        today = datetime.now(tz=pytz.timezone("Europe/Paris"))
        str_today = today.strftime("%Y-%m-%dT%H:%M:%S")
        ## Reponses
        response = requests.get(api_url, 
                                headers={'X-Api-Key': 'YOUR_API_KEY',
                                         'Accept': 'image/jpg'}, stream=True)
        if response.status_code == requests.codes.ok:
            json_data = json.loads(response.text)
            #
            return JsonResponse(data_schedules, status=200, safe=False)
        else :
            return JsonResponse(data, status=400, safe=False)
            
       

class CalendarPrayer(APIView):
    """
    ## Parameters:
    "latitude" (decimal) -
    The decimal value for the latitude co-ordinate of the location you want the time computed for. Example: 51.75865125

    "longitude" (decimal) -
    The decimal value for the longitude co-ordinate of the location you want the time computed for. Example: -1.25387785

    "month" (number) -
    A gregorian calendar month. Example: 8 or 08 for August.

    "year" (number) -
    A gregorian calendar year. Example: 2014.

    "annual" (boolean) -
    If true, we'll ignore the month and return the calendar for the whole year.

    "method" (number) 
    method" (number) -
    A prayer times calculation method. Methods identify various schools of thought about how to compute the timings. If not specified, it defaults to the closest authority based on the location or co-ordinates specified in the API call. This parameter accepts values from 0-12 and 99, as specified below:
    0 - Shia Ithna-Ansari
    1 - University of Islamic Sciences, Karachi
    2 - Islamic Society of North America
    3 - Muslim World League
    4 - Umm Al-Qura University, Makkah
    5 - Egyptian General Authority of Survey
    12 - Union Organization islamic de France
    15 - Moonsighting Committee Worldwide (also requires shafaq paramteer)
    99 - Custom. See https://aladhan.com/calculation-methods
    "shafaq" (string) -
    Which Shafaq to use if the method is Moonsighting Commitee Worldwide. Acceptable options are 'general', 'ahmer' and 'abyad'. Defaults to 'general'.

    "tune" (string) -
    Comma Separated String of integers to offset timings returned by the API in minutes. Example: 5,3,5,7,9,7. See https://aladhan.com/calculation-methods

    "school" (number) -
    0 for Shafi (or the standard way), 1 for Hanafi. If you leave this empty, it defaults to Shafii.

    "midnightMode" (number) -
    0 for Standard (Mid Sunset to Sunrise), 1 for Jafari (Mid Sunset to Fajr). If you leave this empty, it defaults to Standard.

    "timezonestring" (string) -
    A valid timezone name as specified on http://php.net/manual/en/timezones.php . Example: Europe/London. If you do not specify this, we'll calcuate it using the co-ordinates you provide.

    "latitudeAdjustmentMethod" (number) -
    Method for adjusting times higher latitudes - for instance, if you are checking timings in the UK or Sweden.
    1 - Middle of the Night
    2 - One Seventh
    3 - Angle Based

    "adjustment" (number) -
    Number of days to adjust hijri date(s). Example: 1 or 2 or -1 or -2

    "iso8601" (boolean) -
    Whether to return the prayer times in the iso8601 format. Example: true will return 2020-07-01T02:56:00+01:00 instead of 02:56

    Endpoint URL: http://api.aladhan.com/v1/calendar
    Example Request: http://api.aladhan.com/v1/calendar?latitude=51.508515&longitude=-0.1254872&method=2&month=4&year=2017

    """
    permission_classes = [IsAuthorOrReadOnly, ]
    
    def get(self, request, **coordonnees):
         # Using current time
        ini_time_for_now = datetime.now()
        #
        methods = {0 : "Shia Ithna-Ansari",
                  1 : "University of Islamic Sciences, Karachi",
                  2 : "Islamic Society of North America",
                  3 : "Muslim World League",
                  4 : "Umm Al-Qura University, Makkah",
                  5 : "Egyptian General Authority of Survey:",
                  12 : "Union Organization islamic de France",
                  15 : "Moonsighting Committee Worldwide (also requires shafaq paramteer)",
                  99 : "Custom. See https://aladhan.com/calculation-methods"
        }
    
        ## la semaine
        week = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6 : 'saturday'}
        semaine = { 1: "lundi", 2: "mardi", 3:"mercredi", 4: "jeudi", 5: "vendredi", 6: "samedi", 7: "dimanche"
                    }
        ## month dict
        month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 
                       8: 'August', 9: 'September', 10: 'October', 11:'November', 
                       12 : 'December'}
        mois = { 1: "janvier", 2: "fevrier", 3: "mars", 4: "avril", 5: "mai", 6: "juin", 
                 7: "juillet", 8: "aout", 9: "septembre", 10: "octobre", 11: "novembre", 12: "decembre"
                }
        ## get city : (latitude, longitude ) 
        data_in = {
            'country':'France',
            'city':'Lyon',
            'latitude':45.7578137, 
            "longitude": 4.8320114,
            'method':12,
            'month':2,
            'year':2023,
        }
        ##Example Request: http://api.aladhan.com/v1/calendar?latitude=51.508515&longitude=-0.1254872&method=2&month=4&year=2017
        api_url = 'http://api.aladhan.com/v1/calendar?latitude={latitude}&longitude={longitude}&method={method}&month={month}&year={year}'\
            .format(**data_in)
        
        print("API url=", api_url) 
        ## construire struct 
        data_prayer = []
        #today = datetime.utcnow()
        #today = datetime.now(tz=pytz.UTC)
        today = datetime.now(tz=pytz.timezone("Europe/Paris"))
        str_today = today.strftime("%Y-%m-%dT%H:%M:%S")
        start = datetime(today.year, today.month, today.day, 12, 30) 
        str_today = start.strftime("%Y-%m-%dT%H:%M:%S")
        ## Reponses
        response = requests.get(api_url, 
                                headers={'X-Api-Key': 'YOUR_API_KEY',
                                         'Accept': 'image/jpg'}, stream=True)
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text)
            json_data = {}
            data_in.update( {'method': methods[data_in['method']]} )
            data_in.update( {'month':mois[data_in['month']]})
            json_data["settings"] = data_in
            json_data["today"] = data["data"][today.day - 1]
            #json_data["today"] = str_today
            json_data["data"] = data["data"]
            #
            ## {"Fajr": "06:55 (CET)", "Sunrise": "08:03 (CET)", "Dhuhr": "12:54 (CET)", "Asr": "15:22 (CET)", "Sunset": "17:46 (CET)", "Maghrib": "17:46 (CET)", "Isha": "18:53 (CET)", "Imsak": "06:45 (CET)", "Midnight": "00:54 (CET)", "Firstthird": "22:32 (CET)", "Lastthird": "03:17 (CET)"}
            return JsonResponse(json_data, status=200, safe=False)
        else :
            return JsonResponse(data_in, status=400, safe=False)
            
       
 
class GeoCoding(APIView):
    """
    city = 'london'
    api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}'.format(city)
    response = requests.get(api_url + city, headers={'X-Api-Key': 'YOUR_API_KEY'})
    """   
    permission_classes = [IsAuthorOrReadOnly, ]

    def get(self, request, city="Marrakech", country="Fr"):
        #city = 'London'
        #country = 'Fr'
        MY_API_KEY = 'HLaK0UU0DqinZkPLVtNO3Q==zNy0SVxmVjHyqKSa'
        api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(city)
        # https://api.api-ninjas.com/v1/city
        print("API urm =",api_url)
        response = requests.get(api_url, headers={'X-Api-Key': MY_API_KEY })
        if response.status_code == requests.codes.ok:
            json_data = json.loads(response.text)
            return JsonResponse(json_data, status=200, safe=False) 
        else:
            return JsonResponse({}, status=400, safe=False)


    def post(self, request, format=None):
        # serializer = MemberSerializer(data=request.data)
        #
        json_data = {}
        # json_data = json.loads(request.data)
        # json_data = request.data
        print("request.data = ", json_data)
        #return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(json_data, status=200, safe=False)
   

class ParamTimePrayer(APIView):
    queryset = api_models.ParamTimerPrayer.objects.all()
    serializer_class = api_json.ParamTimePrayerSerializer
    permission_classes = (AllowAny, )
    http_method_names = ['post', 'get',]



    
    def post(self, request, format=None):
        # serializer = api_json.ParamTimePrayerSerializer(data=request.data)
        ## print("requets.data : ", request.POST)
        cc = JsonResponseMixin()
        data = dict(request.data)
        # create obj from dict
        data_obj = Dictate(data)
        ##
        json_data = {
            'ville' :  data_obj.geocods.name,
            'pays' :  data_obj.geocods.country, 
            'population' : data_obj.geocods.population,
            'methode' : data_obj.method_selected,
            'longitude': data_obj.geocods.longitude,
            'latitude' : data_obj.geocods.latitude, 
        }
        ## update or create
        try :
            bb, msg_retour = api_models.ParamTimerPrayer.objects.update_or_create(**json_data)
            ## print("retour update_create : ", bb, msg_retour)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as err :
            return Response("error update", status=status.HTTP_400_BAD_REQUEST)

