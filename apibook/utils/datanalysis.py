# -*- coding;UTF-8  -*-
# Data analysis
import os, sys
import pytz
import json
import pylab
import io
import base64
import matplotlib
import csv
import random
from django.utils import timezone
from django.core import serializers

 # from dateutil.parser import *
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from dateutil.rrule import advance_iterator, rrule, DAILY
from django.db import connection
import StringIO
import pandas as pd
from django_pandas.io import read_frame
import matplotlib.pyplot as plt
import matplotlib.pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas, FigureCanvasAgg
import numpy as np
import datetime
from ofschedule import models
from django.contrib.auth.decorators import login_required, permission_required
from planning.settings import PROJECT_PATH


def simple_pandas_matplotlib__(request):
    import matplotlib.pyplot
    import matplotlib.pyplot as plt
    import numpy as np
    from planning.settings import PROJECT_PATH
    from django_pandas.io import read_frame
    import pandas as pd
    #
    matplotlib.use('Agg')
    base_dir_media = PROJECT_PATH + '/media/'
    #
    fig = plt.figure()
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    # OF
    #ofs = models.DjangoOf.objects.filter(statut = 'C').values('machine_travail').distinct().order_by('-semaine')
    ofs = models.DjangoOf.objects.filter(semaine='37', annee='18').values_list(
        'semaine', 'machine_travail_id', 'quantite_prevue').distinct().order_by('semaine')
    # Data Analyse pandas
    df = read_frame(ofs, fieldnames=[
                    'semaine', 'machine_travail_id', 'quantite_prevue'])
    # total des quantite prevue par semaine
    df.groupby('semaine').quantite_prevue.sum()
    # total des quantite prevue par semaine et machine
    df.groupby(['machine_travail_id', 'semaine']).quantite_prevue.sum()

    # df.head(5)
    df[:30].plot()
    x = 0
    h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Plan de charge machine')
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('x label')
    plt.ylabel('y label')
    bar1 = plt.bar(x, h,
                   width=1.0,
                   bottom=0,
                   color='Green',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    response = HttpResponse(df.plot(), content_type='image/png')
    return response


def simple_test_matplotlib(request):
    import matplotlib.pyplot
    import matplotlib.pyplot as plt
    import numpy as np
    from planning.settings import PROJECT_PATH
    from django_pandas.io import read_frame
    import pandas as pd
    import matplotlib
    #
    matplotlib.use('Agg')
    base_dir_media = PROJECT_PATH + '/media/'
    #
    fig = plt.figure()
    buf = io.BytesIO()
    # OF
    ofs = models.DjangoOf.objects.filter(semaine='37', annee='18').values_list(
        'semaine', 'machine_travail_id__nommach', 'quantite_prevue').distinct().order_by('semaine')
    # Data Analyse pandas
    df = read_frame(ofs, fieldnames=[
                    'semaine', 'machine_travail_id', 'quantite_prevue'])

    #x = np.arange(10)
    x = h = []
    for elem in ofs:
        machine, machine, quantite_prevue = elem
        x.append(machine[:1])
        h.append(str(float(quantite_prevue) / 100))

    #h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Plan de charge machine semaine 37')
    #plt.xlim(0, 10)
    #plt.ylim(0, 8)
    plt.xlabel('Machines')
    plt.ylabel('quantite prevue')
    bar1 = plt.bar(x, h,
                   width=0.5,
                   bottom=0,
                   color='Blue',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)

    with open(os.path.join(base_dir_media, "testPlot.png"), "wb") as fd:
        fd.write(buf.getvalue())

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response


def mplimage1(request):

    # 1-
    # matplotlib.use('Agg')
    ofs = models.DjangoOf.objects.filter(semaine='38', annee='18')

    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_commandee'])
    plt.legend()
    # 3-
    fig = matplotlib.figure.Figure()

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(fig)
    matplotlib.pyplot.close(fig)
    buffer = cStringIO.StringIO()
    cropped_img.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())
    return HttpResponse(img_str, content_type='image/png')

#@api.multi


def mplimage2(request, kind):

    # 1-
    # matplotlib.use('Agg')
    ofs = models.DjangoOf.objects.filter(semaine='38', annee='18')

    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_commandee'])

    if kind == "1":
        df.plot(kind="line", stacked=True)
    elif kind == 2:
        df.plot(kind="bar", stacked=True)
    elif kind == "3":
        df.plot(kind="barh", stacked=True)
    elif kind == "4":
        df.plot(kind="kde", stacked=True)
    elif kind == "5":
        df.plot(kind="density", stacked=True)
    elif kind == "6":
        df.plot(kind="area", stacked=True)
    else:
        df.plot(kind="bar", stacked=True)

    # 2 --
    dfg = df.groupby('machine_travail')
    rs = dfg.sum(level='machine_travail')

    x = list(rs.axes[0])
    columns = list(df.columns)
    h = [2900.0, 5000.0,    3000.0,  5000.0, 10083.0, 13500.0,
         4470.0, 10083.0,  2500.0,  5500.0,  8321.0, 12000.0]
    #h = x
    plt.title(columns)
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('Machine Conditionnment')
    plt.ylabel('Quantite commandee')
    bar1 = plt.bar(x, h,
                   width=1.0,
                   bottom=0,
                   color='green',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    # 3-
    fig = matplotlib.figure.Figure()

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    matplotlib.pyplot.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    # if required clear the figure for reuse
    # Register a function to be run once
    fig.clear()
    return response
#----------------------
# MATPLOTLIB
#--------------------
def simple_pandas_matplotlib(request):
    #
    response = HttpResponse("ok...", content_type='image/png')
    return response


def simple_pandas_matplotlib__(request):
    import matplotlib.pyplot
    import matplotlib.pyplot as plt
    import numpy as np
    from planning.settings import PROJECT_PATH
    from django_pandas.io import read_frame
    import pandas as pd
    #
    matplotlib.use('Agg')
    base_dir_media = PROJECT_PATH + '/media/'
    #
    fig = plt.figure()
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    # OF
    #ofs = models.DjangoOf.objects.filter(statut = 'C').values('machine_travail').distinct().order_by('-semaine')
    ofs = models.DjangoOf.objects.filter(semaine='37', annee='18').values_list(
        'semaine', 'machine_travail_id', 'quantite_prevue').distinct().order_by('semaine')
    # Data Analyse pandas
    df = read_frame(ofs, fieldnames=[
                    'semaine', 'machine_travail_id', 'quantite_prevue'])
    # total des quantite prevue par semaine
    df.groupby('semaine').quantite_prevue.sum()
    # total des quantite prevue par semaine et machine
    df.groupby(['machine_travail_id', 'semaine']).quantite_prevue.sum()

    # df.head(5)
    df[:30].plot()
    x = 0
    h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Plan de charge machine')
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('x label')
    plt.ylabel('y label')
    bar1 = plt.bar(x, h,
                   width=1.0,
                   bottom=0,
                   color='Green',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    response = HttpResponse(df.plot(), content_type='image/png')
    return response


def simple_test_matplotlib(request):
    import matplotlib.pyplot
    import matplotlib.pyplot as plt
    import numpy as np
    from planning.settings import PROJECT_PATH
    from django_pandas.io import read_frame
    import pandas as pd
    import matplotlib
    #
    matplotlib.use('Agg')
    base_dir_media = PROJECT_PATH + '/media/'
    #
    fig = plt.figure()
    buf = io.BytesIO()
    # OF
    ofs = models.DjangoOf.objects.filter(semaine='37', annee='18').values_list(
        'semaine', 'machine_travail_id__nommach', 'quantite_prevue').distinct().order_by('semaine')
    # Data Analyse pandas
    df = read_frame(ofs, fieldnames=[
                    'semaine', 'machine_travail_id', 'quantite_prevue'])

    #x = np.arange(10)
    x = h = []
    for elem in ofs:
        machine, machine, quantite_prevue = elem
        x.append(machine[:1])
        h.append(str(float(quantite_prevue) / 100))

    #h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Plan de charge machine semaine 37')
    #plt.xlim(0, 10)
    #plt.ylim(0, 8)
    plt.xlabel('Machines')
    plt.ylabel('quantite prevue')
    bar1 = plt.bar(x, h,
                   width=0.5,
                   bottom=0,
                   color='Blue',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)

    with open(os.path.join(base_dir_media, "testPlot.png"), "wb") as fd:
        fd.write(buf.getvalue())

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response


def mplimage1(request):

    # 1-
    # matplotlib.use('Agg')
    ofs = models.DjangoOf.objects.filter(semaine='38', annee='18')

    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_commandee'])
    plt.legend()
    # 3-
    fig = matplotlib.figure.Figure()

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(fig)
    matplotlib.pyplot.close(fig)
    buffer = cStringIO.StringIO()
    cropped_img.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())
    return HttpResponse(img_str, content_type='image/png')

#@api.multi


def mplimage2(request, kind):

    # 1-
    # matplotlib.use('Agg')
    ofs = models.DjangoOf.objects.filter(semaine='38', annee='18')

    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_commandee'])

    if kind == "1":
        df.plot(kind="line", stacked=True)
    elif kind == 2:
        df.plot(kind="bar", stacked=True)
    elif kind == "3":
        df.plot(kind="barh", stacked=True)
    elif kind == "4":
        df.plot(kind="kde", stacked=True)
    elif kind == "5":
        df.plot(kind="density", stacked=True)
    elif kind == "6":
        df.plot(kind="area", stacked=True)
    else:
        df.plot(kind="bar", stacked=True)

    # 2 --
    dfg = df.groupby('machine_travail')
    rs = dfg.sum(level='machine_travail')

    x = list(rs.axes[0])
    columns = list(df.columns)
    h = [2900.0, 5000.0,    3000.0,  5000.0, 10083.0, 13500.0,
         4470.0, 10083.0,  2500.0,  5500.0,  8321.0, 12000.0]
    #h = x
    plt.title(columns)
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('Machine Conditionnment')
    plt.ylabel('Quantite commandee')
    bar1 = plt.bar(x, h,
                   width=1.0,
                   bottom=0,
                   color='green',
                   alpha=0.65,
                   label='Legend')
    plt.legend()

    # 3-
    fig = matplotlib.figure.Figure()

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    matplotlib.pyplot.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    # if required clear the figure for reuse
    # Register a function to be run once
    fig.clear()
    return response


def construct_columns(mes_columns):
    """
    construit un tableau columns pour bootstrap_table
    """
    columns = [{'field':  elem, 'title': elem, 'type':   'datetime'}
               for elem in mes_columns]
    return columns


def PandasOfView(request):
  template = 'pandas_of.html'

  qs = models.DjangoOf.objects.filter(semaine='38', annee='18').values_list(
      'code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
  #df = qs.to_dataframe()
  df = read_frame(qs, fieldnames=['machine_travail', 'quantite_commandee'])
  dfg = df.groupby(df['machine_travail']).sum()

  # trier par quantitee
  dfg.sort_values('quantite_commandee')
  indexes = list(dfg.axes[0])

  data = [{'field':  index, 'title': elem} for index, elem in dfg]
  columns = construct_columns(df.columns)

  #Format the column headers for the Bootstrap table, they're just a list of field names,
  #duplicated and turned into dicts like this: {'field': 'foo', 'title: 'foo'}
  #columns = [{'field': champ, 'title': champ} for champ in DjangoOf._meta.get_fields()]

  #Write the DataFrame to JSON (as easy as can be)
  # output just the records (no fieldnames) as a collection of tuples
  json = dfg.to_json(orient='records')
  #Proceed to create your context object containing the columns and the data
  context = {
             'data': json,
             'columns': columns
            }
  #And render it!
  return render(request, template, context)


#@method_decorator(login_required, 'dispatch')
@permission_required('ofschedule.change_djangoof', login_url="/admin/login/")
def console_admin(request):
    """
    """
    template = "console/console_admin.html"
    #And render it!
    context = dict()
    return render(request, template, context)


def query_of(request):
    """
    console de requete of
    """
    template = "console/of_crud.html"
    #And render it!
    context = dict()

    #qs = models.DjangoOf.objects.filter(semaine='38', annee='18' ).values_list('code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
    qs = models.DjangoOf.objects.filter(annee='18').order_by(
        '-date_debut_reelle')  # Use the Pandas Manager
    #df = read_frame(qs, fieldnames = ['machine_travail', 'quantite_commandee'])
    df = read_frame(qs,
                    fieldnames=['id', 'code_of', 'statut', 'date_debut_reelle', 'semaine', 'annee',
                                'commande_id', 'machine_travail', 'client_id', 'quantite_prevue', 'quantite_commandee',
                                'quantite_realisee'])
    # entete de colonnes
    columns = construct_columns(df.columns)
    #Write the DataFrame to JSON (as easy as can be)
    #json = dfg.to_json(orient='records')  # output just the records (no fieldnames) as a collection of tuples
    # output just the records (no fieldnames) as a collection of tuples
    json = df.to_json(orient='records')
    #Proceed to create your context object containing the columns and the data
    context = {
             'data': json,
             'columns': columns
            }
    return render(request, template, context)


def query_logging(request):
    """
    console de requete log
    """
    template = "console/of_crud.html"
    #And render it!
    context = dict()

    #qs = models.DjangoOf.objects.filter(semaine='38', annee='18' ).values_list('code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
    qs = models.DjangoLogging.objects.all().order_by('-id')  # Use the Pandas Manager
    #df = read_frame(qs, fieldnames = ['machine_travail', 'quantite_commandee'])
    columns = [f.name for f in models.DjangoLogging._meta.get_fields()]

    df = read_frame(qs, fieldnames=[
                    'id', 'code_erreur', 'programme_name', 'statut', 'description', 'created', 'created_by'])
    # entete de colonnes
    columns = construct_columns(df.columns)
    #Write the DataFrame to JSON (as easy as can be)
    #json = dfg.to_json(orient='records')  # output just the records (no fieldnames) as a collection of tuples
    # output just the records (no fieldnames) as a collection of tuples
    json = df.to_json(orient='records')
    #Proceed to create your context object containing the columns and the data
    context = {
             'data': json,
             'columns': columns
            }
    return render(request, template, context)


def dictfetchall(sql):
    "Return all rows from a cursor as a dict"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        all_columns = [str(col[0]) for col in cursor.description]
        #
        data = [dict(zip(all_columns, row)) for row in cursor.fetchall()]
        # on traite les date
        data_clean = []
        for row in data:
            for columns, elem in row.items():
                if (type(elem) == datetime.date or type(elem) == datetime.datetime) and elem != None:
                                row[columns] = elem.isoformat()
            # recharge  data new
            data_clean.append(row)

        return all_columns, data_clean


def my_custom_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    return rows

#@method_decorator(login_required, 'dispatch')
#@permission_required('ofschedule.change_djangoof')


def dba_query(request, requete):
    """
    console de requete constraints name
    """
    template = "console/of_crud.html"
    #And render it!
    context = dict()

    # sql = " SELECT * FROM sys.objects "
    # df = models.DjangoOf.objects.filter(semaine='38', annee='18' ).values_list('code_of', 'commande_id', 'machine_travail_id')  # Use the Pandas Manager
    #rows = DjangoLogging.objects.raw("select * from categorie_transmission")   # Use the Pandas Manager
    if requete == '1':  # liste des foreighkey
        sql1 = "EXEC sp_fkeys 'transmission'"
        sql = "SELECT OBJECT_NAME(object_id) AS ConstraintName, SCHEMA_NAME(schema_id) AS SchemaName, type_desc AS ConstraintType FROM sys.objects WHERE SCHEMA_NAME(schema_id)='dbo'"
        sql3 = "SELECT OBJECT_NAME(object_id) AS ConstraintName, SCHEMA_NAME(schema_id) AS SchemaName, OBJECT_NAME(parent_object_id) AS TableName, type_desc AS ConstraintType FROM sys.objects WHERE type_desc LIKE '%CONSTRAINT%'"

    elif requete == '2':  # ligne de PDC
        sql = """
        SELECT TOP(10000)  * FROM tmpcharc
        WHERE ancond > '17'
        ORDER BY id DESC
        """

    elif requete == '3':  # Fiche de travail
        sql = """
        SELECT TOP(10000)  codefcndt, code_of, datecndt, codeartc, codecndt, cdesce, nbreacndt,
        nbrecndt, qteacndt, qtecndt, qtestock, datedcndt
        FROM ficwcndt
        WHERE cdesce IS NOT NULL and datecndt IS NOT NULL
        ORDER BY codefcndt DESC
        """

    elif requete == '4':
        sql = "SELECT TOP(1000) * FROM  ligappro ORDER BY cdeappro DESC,  lignappr  DESC"

    elif requete == '5':
        sql = """
        SELECT TOP(10000) * FROM  cde_clie
        WHERE ancond > '17'
        ORDER BY datepcnd DESC
        """

    elif requete == '6':  # doublons OFs
        sql = """
        SELECT * FROM ordre_fabrication WHERE code_of IN (
            SELECT  code_of
            FROM ordre_fabrication
            WHERE code_of is not null
            GROUP BY  code_of
            HAVING count(code_of) > 1
            )
        ORDER BY count(code_of) DESC
        """
    elif requete == '7':  # doublons OFs
        sql = """
            SELECT * FROM tmpcharc WHERE cdsce IN (
            SELECT cdesce, count(code_of) as nb
            FROM tmpcharc
            WHERE code_of is not null
            GROUP BY  cdesce,  code_of
             HAVING count(code_of) > 1
             )
             ORDER BY count(code_of) DESC
             """
    elif requete == '8':  # doublons OFs
        sql = """
            SELECT * FROM ordre_fabrication WHERE code_of NOT IN(
                SELECT  code_of
                FROM tmpcharc
                WHERE code_of is not null
             )
             ORDER BY count(code_of) DESC
             """
    elif requete == '9':  # Liste des view
        sql = """
            select O.name as [Object_Name], C.text as [Object_Definition]
            from sys.syscomments C
            inner join sys.all_objects O ON C.id = O.object_id
            --where C.text like '%table_name%'
            """
    elif requete == '10':  # liste des coloumns
        sql = "EXEC sp_columns 'ordre_fabrication'"
    else:
        sql = " SELECT TOP(100) * FROM sys.objects "

    # execute curseur
    all_columns, rows = dictfetchall(sql)
    #

    columns = ['id', 'created', 'libelle', 'description']
    # output just the records (no fieldnames) as a collection of tuples
    json_data = json.dumps(rows)
    #Proceed to create your context object containing the columns and the data
    context = {
             'data': json_data,
             'columns': construct_columns(all_columns)

            }
    return render(request, template, context)


def plot_of_test(request):

    # ex donne en 4 :   df2 = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
    # df2.plot.bar()

    # 1-
    fig = matplotlib.figure.Figure()
    canvas = FigureCanvasAgg(fig)

    # 2- canvas
    #buf = io.BytesIO()
    #canvas.print_png(buf)

    ofs = models.DjangoOf.objects.filter(semaine='38', annee='18')

    # df = pd.DataFrame(ofs, columns = ['code_of', 'quantite_commandee'] )
    df = read_frame(ofs, fieldnames=['machine_travail', 'quantite_prevue'])
    #df.plot(ax=ax)
    df.plot(kind="bar", stacked=True)
    #plt.show()

    base_dir_media = PROJECT_PATH + '/media/'
    """

    with open(os.path.join(base_dir_media, "testPlot.png"), "wb") as fd_image :
        fd_image.write(buf.getvalue())
        #

        with open(os.path.join(base_dir_media, "testPlot.png"), "rb") as fd :
            response = HttpResponse(fd, content_type = 'image/png')
            #pylab.savefig(response, format="png")
    """

    output = StringIO.StringIO()
    fig.savefig(output, format="png")
    contents = output.getvalue()

    #
    plt.close(fig)
    response = HttpResponse(contents, content_type='image/png')
    #canvas.print_png(response)

    # 3 print
    #df.plot(kind="bar", stacked=True)
    #canvas.print_png(response)
    # plot  df.plot(kind='bar')
    # df.plot.hist(alpha=0.5)

    # hitogramme des ofs
    #plt.axhline(0, color='k')
    #plt.show()
    return response



def export_as_json(request, ct, ids):
    queryset = models.DjangoOf.objects.filter(id__in=ids.split(","))
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

from django.utils.encoding import smart_str

def export_as_cvs(request, ct, ids):
    queryset = models.DjangoOf.objects.filter(id__in=ids.split(","))
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    # response['Content-Disposition'] = 'attachment; filename="%s"'% os.path.join('export', 'export_of.csv')
    writer = csv.writer(response)
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.code_of),
            smart_str(obj.client),
        ])
    return response
