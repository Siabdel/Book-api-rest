# -*- coding:UTF-8 -*-
from __future__ import unicode_literals
# Data analysis
import os, sys
import datetime
import pytz
import json
import pylab
import io
import base64
import matplotlib
import csv
import random
import subprocess
import codecs
from codecs import open as opencodecs
from io import BytesIO
from dateutil.rrule import advance_iterator, rrule, DAILY
# pandas
import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas, FigureCanvasAgg
import numpy as np
import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
from django_pandas.io import read_frame
import pandas as pd

 # from dateutil.parser import *
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core import serializers
from django.views.generic.edit import UpdateView, CreateView, DeleteView, ModelFormMixin, ProcessFormView, FormView, FormMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib import messages
# local
from planning.settings import PROJECT_PATH
from planning import settings

from ofschedule import models
from unidecode import unidecode  # pour finir avec les chaine accentué
# pdf file
import pdfkit as pdf_kit
from django.template.loader import get_template
from django.template import Context
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
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


def export_as_json(request, ct, ids):
    queryset = models.DjangoOf.objects.filter(id__in=ids.split(","))
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

def html_to_pdf(request, queryset):
    """
    genere un pdf a partir d'un fichier HTML
    """
    pdf_filename = os.path.join(settings.MEDIA_ROOT, 'printout.pdf')
    html_filename = os.path.join(settings.MEDIA_ROOT, 'printout.html')
    # contruire le template
    template = get_template('easy_pdf/test_pdf.html')
    # re.UNICODE

    # ecrire entete du fichier avec les libelles
    all_columns =  all_columns_panda(queryset)
    # writer.writerow(all_columns)

    # Ecrire les valeurs du queryset
    ind = 0
    data_dict = all_records_panda(queryset, fields=all_columns)
    # messages.add_message(self.request, messages.INFO, 'elem *** = %s' % data_dict)
    #Proceed to create your context object containing the columns and the data
    context = {
             'data': data_dict,
             'columns': all_columns
            }

    result = template.render( {'object_list':queryset})
    # Save en HTM
    with opencodecs(html_filename, 'w', 'utf-8') as fd_out:
        fd_out.write(result)

    # save en pdf
    # production du pdf sous shell avec wkhtmltopdf
    # wkhtmltopdf
    try :
        #subprocess.call(["firefox", "out/cv_format_%s.html" % cv_id])
        os.system("wkhtmltopdf {} {}".format(html_filename, pdf_filename))
    except err:
        messages.success(request, "oups erreur ! %s ... " % err.message)
    except Exception, err:
        messages.success(request, "oups erreur ! %s ... " % err.message)

    # affichage
    with opencodecs(pdf_filename, 'r') as fd_pdf:
        fd_pdf = fd_pdf.read()

    response = HttpResponse(fd_pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response


#-----------------------------------------------
# lancer subprocess sans fenetre dos
#----------------------------------------------
def launchWithoutConsole(command, args):
    """Launches 'command' windowless and waits until finished"""
    #startupinfo = subprocess.STARTUPINFO
    #startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #
    return subprocess.Popen([command] + args).wait()
#-----------------------------------------------
# view fichier pdf
#----------------------------------------------
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class MonEmailAdapter(object):
    """
    """
    def format_email_subject(self, subject):
        prefix = settings.EMAIL_SUBJECT_PREFIX
        if prefix is None:
            site = get_current_site()
            prefix = "[{name}] ".format(name=site.name)
        return prefix + force_text(subject)

    def render_mail(self, template_prefix, email, context):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        subject = render_to_string('{0}.txt'.format(template_prefix), context)

        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        bodies = {}
        for ext in ['html', 'txt']:
            try:
                template_name = '{0}_message.{1}'.format(template_prefix, ext)
                bodies[ext] = render_to_string(template_name, context).strip()
            except TemplateDoesNotExist:
                if ext == 'txt' and not bodies:
                    # We need at least one body
                    raise


        if  'html' in bodies:


            """
            A version of EmailMessage that makes it easy to send multipart/alternative
            messages. For example, including text and HTML versions of the text is
            made easier.

            alternative_subtype = 'alternative'

            __init__( subject='', body='', from_email=None, to=None, bcc=None,
            connection=None, attachments=None, headers=None, alternatives=None,
            cc=None, reply_to=None):

            Initialize a single email message (which can be sent to multiple
            recipients).
            """



            msg = EmailMultiAlternatives(subject,
                                         bodies['txt'],
                                         settings.DEFAULT_FROM_EMAIL,
                                         [email])
            if 'html' in bodies:
                msg.attach_alternative(bodies['html'], 'text/html')

        elif  'txt' in bodies:
            msg = EmailMessage(subject,
                               bodies['txt'],
                               settings.DEFAULT_FROM_EMAIL,
                               [email])
            msg.content_subtype = 'txt'  # Main content is now text/html
        #
        return msg

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        msg.send()


    def get_email_confirmation_redirect_url(self, request):
        """
        The URL to return to after successful e-mail confirmation.
        """
        if request.user.is_authenticated():
            if app_settings.EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL:
                return  \
                    app_settings.EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL
            else:
                return self.get_login_redirect_url(request)
        else:
            return app_settings.EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL


    def clean_email(self, email):
        """
        Validates an email value. You can hook into this if you want to
        (dynamically) restrict what email addresses can be chosen.
        """
        return email


    def add_message(self, request, level, message_template,
                    message_context=None, extra_tags=''):
        """
        Wrapper of `django.contrib.messages.add_message`, that reads
        the message text from a template.
        """
        if 'django.contrib.messages' in settings.INSTALLED_APPS:
            try:
                if message_context is None:
                    message_context = {}
                message = render_to_string(message_template,
                                           message_context).strip()
                if message:
                    messages.add_message(request, level, message,
                                         extra_tags=extra_tags)
            except TemplateDoesNotExist:
                pass

    def ajax_response(self, request, response, redirect_to=None, form=None):
        data = {}
        status = response.status_code

        if redirect_to:
            status = 200
            data['location'] = redirect_to
        if form:
            if form.is_valid():
                status = 200
            else:
                status = 400
                data['form_errors'] = form._errors
            if hasattr(response, 'render'):
                response.render()
            data['html'] = response.content.decode('utf8')
        return HttpResponse(json.dumps(data),
                            status=status,
                            content_type='application/json')



    def is_safe_url(self, url):
        from django.utils.http import is_safe_url
        return is_safe_url(url)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "account_confirm_email",
            args=[emailconfirmation.key])
        ret = build_absolute_uri(
            request,
            url,
            protocol=app_settings.DEFAULT_HTTP_PROTOCOL)
        return ret

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(
            request,
            emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": "atlasRDV",
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = 'account/email/email_confirmation_signup'
        else:
            email_template = 'account/email/email_confirmation'
        self.send_mail(email_template,
                       emailconfirmation.email_address.email,
                       ctx)
# appel de la class MonEmail Adapter
def get_adapter():
    return MonEmailAdapter()

# exemple utilisation de l'adapteur Email
def _ajax_response(request, response, form=None):
    if request.is_ajax():
        if (isinstance(response, HttpResponseRedirect)
                or isinstance(response, HttpResponsePermanentRedirect)):
            redirect_to = response['Location']
        else:
            redirect_to = None
        response = get_adapter().ajax_response(request,
                                               response,
                                               form=form,
                                               redirect_to=redirect_to)
    return response



def all_columns_class(queryset):
    """
    donne un tableau des colonne d'une class tableExport
    """

    nom_class = queryset.first().__class__
    # ecrire entete du fichier avec les libelles
    # all_columns =  dict([(fld.name, fld.name) for fld in nom_class._meta.fields ])
    all_columns = [ smart_str(fld.name)  for fld in nom_class._meta.fields ]
    return all_columns

def all_columns_panda(queryset):
    """
    donne un tableau des colonne d'une class tableExport
    """
    df = read_frame(queryset)
    cols = df.columns
    all_columns = [ smart_str(elem) for elem in cols.format() ]
    return all_columns

def all_records_panda(queryset, fields=None):
    """
    donne un tableau des values
    """
    if fields :
        df = read_frame(queryset, fieldnames= fields)
    else:
        df = read_frame(queryset)

    # une list records
    records = df.to_dict('records')

    # traitement des pb encodage ascii en error
    all_record = []

    for ligne in records:
        ligne_value = []
        #ligne = dict([( lib.upper(), unidecode(val)) for lib, val in ligne.items() if val != None])
        for lib, val in ligne.items():
            if val == None:
                val = ""
            elif type(val) == type(""):
                val = unidecode(val)
            elif isinstance(val, datetime.datetime.fromtimestamp.__class__):
                val = datetime.fromtimestamp(val)
                val = val.strftime('%d/%m/%Y')

            ligne_value.append((lib.upper(), val))
        # recontruit tableau des dict
        all_record.append(dict(ligne_value))

    # retour
    return all_record
