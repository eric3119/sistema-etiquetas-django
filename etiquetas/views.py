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

    etiquetas = Etiqueta.objects.order_by('id')

    count_enviados = len(Etiqueta.objects.exclude(data_gerado=None))
    count_pendentes = 0

    try:
        count_pendentes = len(Etiqueta.objects.filter(data_gerado=None))
    except Etiqueta.DoesNotExist:
        pass
    
    return render(request, 'etiquetas.html', {
        'title': 'Sistema de etiquetas',
        'etiquetas': etiquetas,
        'count_enviados': count_enviados,
        'count_pendentes': count_pendentes,
    })

def envios(request):

    etiquetas = Etiqueta.objects.exclude(data_gerado=None)

    count_enviados = len(etiquetas)
    count_pendentes = 0

    try:
        count_pendentes = len(Etiqueta.objects.filter(data_gerado=None))
    except Etiqueta.DoesNotExist:
        pass
    
    return render(request, 'etiquetas.html', {
        'title': 'Enviados',
        'etiquetas': etiquetas,
        'count_enviados': count_enviados,
        'count_pendentes': count_pendentes,
    })

def pendentes(request):

    count_enviados = len(Etiqueta.objects.exclude(data_gerado=None))
    count_pendentes = 0
    
    try:
        etiquetas = Etiqueta.objects.filter(data_gerado=None)
        count_pendentes = len(etiquetas)
    except Etiqueta.DoesNotExist:
        etiquetas = None
    
    return render(request, 'etiquetas.html', {
        'title': 'Pendentes',
        'etiquetas': etiquetas,
        'count_enviados': count_enviados,
        'count_pendentes': count_pendentes,
    })

def get_etiq(request, id_etiq):

    erros = []    

    try:
        etiqueta = Etiqueta.objects.get(id=id_etiq)
    except Etiqueta.DoesNotExist:
        etiqueta = None
        erros.append('Não existe')
    
    return render(request, 'etiq_item.html', {
        'etiqueta': etiqueta,
        'erros': erros,
        'title': 'Detalhes'
    })

def delete_etiq(request, id_etiq):

    try:
        etiqueta = Etiqueta.objects.get(id=id_etiq)
        etiqueta.delete()
    except Etiqueta.DoesNotExist:        
        return HttpResponseRedirect('/erro')
    
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
        'title': 'Adicionar'
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
        'title': 'Atualizar'
    })

def pdf_gen(request, id_etiq):

    etiqueta = Etiqueta.objects.get(id=id_etiq)
    
    width, height = A4
    linha = 15

    title = 'etiqueta{}'.format(etiqueta.id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="'+title+'.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    p.setTitle(title)
    #p.rect(inch, inch, width-2*inch, height-2*inch)
    p.drawString(inch, height-inch, 'Nome: '+etiqueta.nome)
    p.drawString(inch, height-inch-linha, 'Função: '+etiqueta.funcao)
    p.drawString(inch, height-inch-2*linha, 'Email: '+etiqueta.email)
    p.drawString(inch, height-inch-3*linha, 'Orgão: '+etiqueta.orgao)
    p.drawString(inch, height-inch-4*linha, 'Endereco: '+etiqueta.endereco)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    if etiqueta.data_gerado == None:
        etiqueta.data_gerado = timezone.now()
        etiqueta.save()

    return response

def erro(request):
    return render(request, 'erro.html', {
        'teste': 'teste'
    })