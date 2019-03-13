from django.shortcuts import render
from .models import Destinatario, Remetente
from .forms import EtiqForm, DestinatarioForm, RemetenteForm

import io
from django.http import FileResponse, HttpResponse, HttpResponseRedirect

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm


from django.utils import timezone
import pytz

import logging
logger = logging.getLogger(__name__)

def home(request):

    etiquetas = Destinatario.objects.order_by('id')

    count_enviados = len(Destinatario.objects.exclude(data_gerado=None))
    count_pendentes = 0

    try:
        count_pendentes = len(Destinatario.objects.filter(data_gerado=None))
    except Destinatario.DoesNotExist:
        pass
    
    return render(request, 'etiquetas.html', {
        'title': 'Sistema de etiquetas',
        'etiquetas': etiquetas,
        'count_enviados': count_enviados,
        'count_pendentes': count_pendentes,
    })

def envios(request):

    etiquetas = Destinatario.objects.exclude(data_gerado=None)

    count_enviados = len(etiquetas)
    count_pendentes = 0

    try:
        count_pendentes = len(Destinatario.objects.filter(data_gerado=None))
    except Destinatario.DoesNotExist:
        pass
    
    return render(request, 'etiquetas.html', {
        'title': 'Enviados',
        'etiquetas': etiquetas,
        'count_enviados': count_enviados,
        'count_pendentes': count_pendentes,
    })

def pendentes(request):

    count_enviados = len(Destinatario.objects.exclude(data_gerado=None))
    count_pendentes = 0
    
    try:
        etiquetas = Destinatario.objects.filter(data_gerado=None)
        count_pendentes = len(etiquetas)
    except Destinatario.DoesNotExist:
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
        etiqueta = Destinatario.objects.get(id=id_etiq)
    except Destinatario.DoesNotExist:
        etiqueta = None
        erros.append('Não existe')
    
    return render(request, 'etiq_item.html', {
        'etiqueta': etiqueta,
        'erros': erros,
        'title': 'Detalhes'
    })

def delete_etiq(request, id_etiq):

    id_remetente = None

    try:        
        etiqueta = Destinatario.objects.get(id=id_etiq)
        id_remetente = etiqueta.id_remetente
        etiqueta.delete()        
    except Destinatario.DoesNotExist:        
        return HttpResponseRedirect('/erro')
    
    if remetente:
        remetente = Remetente.objects.get(id=id_remetente)
        remetente.delete()
        return HttpResponseRedirect('/')

def create_etiq(request):

    count_enviados = len(Destinatario.objects.exclude(data_gerado=None))
    count_pendentes = 0

    try:
        count_pendentes = len(Destinatario.objects.filter(data_gerado=None))
    except Destinatario.DoesNotExist:
        pass

    if request.method == 'POST':        
        form = EtiqForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    
    else:
        form = EtiqForm()
    
    return render(request, 'etiq_form.html', {
        'form': form,
        'title': 'Adicionar Destinatário',
        'count_enviados': count_enviados,
        'count_pendentes': count_pendentes,
    })

def update_etiq(request, id_etiq):

    etiqueta = Destinatario.objects.get(id=id_etiq)
    
    if request.method == 'POST':
        form = EtiqForm(request.POST)

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

    destinatario = Destinatario.objects.get(id=id_etiq)
    remetente = None
    try:
        remetente = Remetente.objects.get(id=destinatario.id_remetente)
    except Remetente.DoesNotExist:
        pass
    
    if not remetente:

        if request.method == 'POST':
            form = RemetenteForm(request.POST)

            if form.is_valid():            
                new_dest = form.save()
                Destinatario.objects.filter(id=id_etiq).update(id_remetente=new_dest.pk)
            return HttpResponseRedirect('/pdf/{}'.format(id_etiq))
        else:
            return render(request, 'etiq_form.html', {
                'form': RemetenteForm(),
                'title': 'Remetente'
            })

    width, height = A4

    title = 'etiqueta{}'.format(destinatario.id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="'+title+'.pdf"'

    buffer = io.BytesIO()

    linhas_destinatario = [
        'Destinatário',
        'Nome: '+destinatario.nome,
        'Função: '+destinatario.funcao,
        'Email: '+destinatario.email,
        'Orgão: '+destinatario.orgao,
        'Endereco: '+destinatario.endereco,
        '',
    ]
    linhas_remetente= [
        'Remetente',
        'Nome: '+remetente.nome,
        'Função: '+remetente.funcao,
        'Email: '+remetente.email,
        'Orgão: '+remetente.orgao,
        'Endereco: '+remetente.endereco
    ]

    tam_linha = 15
    linha = 0

    p = canvas.Canvas(buffer)
    
    p.setTitle(title)

    p.rect(inch, inch, width-2*inch, height-2*inch+tam_linha)

    for x in linhas_destinatario:
       p.drawString(inch, height-inch-linha*tam_linha, x)
       linha+=1

    for x in linhas_remetente:
       p.drawString(inch, height-inch-linha*tam_linha, x)
       linha+=1   

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    if destinatario.data_gerado == None:
        destinatario.data_gerado = timezone.now()
        destinatario.save()

    return response

def erro(request):
    return render(request, 'erro.html', {
        'teste': 'teste'
    })