from django.shortcuts import render
from .models import Etiqueta

import io
from django.http import FileResponse, HttpResponse, HttpResponseRedirect

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm

from .forms import EtiqForm

from django.utils import timezone
import pytz

import logging
logger = logging.getLogger(__name__)

def home(request):

    nome = 'django'

    etiquetas = Etiqueta.objects.order_by('id')
    
    return render(request, 'etiquetas.html', {
        'nome': nome,
        'etiquetas': etiquetas
    })

def envios(request):

    nome = 'envios'

    etiquetas = Etiqueta.objects.exclude(data_gerado=None)
    
    return render(request, 'envios.html', {
        'nome': nome,
        'etiquetas': etiquetas
    })

def get_etiq(request, id_etiq):
    etiqueta = Etiqueta.objects.get(id=id_etiq)
    
    return render(request, 'etiq_item.html', {
        'etiqueta': etiqueta
    })

def delete_etiq(request, id_etiq):
    etiqueta = Etiqueta.objects.get(id=id_etiq)
    etiqueta.delete()    
    
    return HttpResponseRedirect('/')

def create_etiq(request):

    if request.method == 'POST':        
        form = EtiqForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    
    else:
        form = EtiqForm()
    
    return render(request, 'etiq_form.html', {
        'form': form,
    })

def update_etiq(request, id_etiq):

    etiqueta = Etiqueta.objects.get(id=id_etiq)
    
    if request.method == 'POST':
        form = EtiqForm(request.POST, instance=etiqueta)

        if form.is_valid():            
            form.save()
            return HttpResponseRedirect('/etiqueta/{}'.format(id_etiq))
    
    else:        
        form = EtiqForm(instance=etiqueta)
    
    return render(request, 'etiq_form.html', {
        'form': form,
    })

def pdf_gen(request, id_etiq):

    etiqueta = Etiqueta.objects.get(id=id_etiq)
    width, height = A4    

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="'+etiqueta.nome+'.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    #p.rect(inch, inch, width-2*inch, height-2*inch)
    p.drawString(inch, height-inch, 'nome: '+etiqueta.nome)
    p.drawString(inch, height-inch-cm, 'funcao: '+etiqueta.funcao)
    p.drawString(inch, height-inch-2*cm, 'email: '+etiqueta.email)
    p.drawString(inch, height-inch-3*cm, 'orgao: '+etiqueta.orgao)
    p.drawString(inch, height-inch-4*cm, 'endereco: '+etiqueta.endereco)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    if etiqueta.data_gerado == None:
        etiqueta.data_gerado = timezone.now()
        etiqueta.save()

    return response