from django.shortcuts import render
from .models import Destinatario, Remetente
from .forms import DestinatarioForm, RemetenteForm

import io
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, Http404

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm


from django.utils import timezone
import pytz

import logging
logger = logging.getLogger(__name__)

from django.views.generic import TemplateView, ListView, DetailView, UpdateView

class DestinatariosView(ListView):

    model=Destinatario
    template_name = 'destinatarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count_enviados'] = len(Destinatario.objects.exclude(data_gerado=None))         
        try:
            context['count_pendentes'] = len(Destinatario.objects.filter(data_gerado=None))
        except Destinatario.DoesNotExist:
            context['count_pendentes'] = 0

        return context

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

class DestinatarioDetailView(DetailView):
    model=Destinatario
    template_name='etiq_item.html'

def delete_etiq(request, id_etiq):

    id_remetente = None

    try:        
        etiqueta = Destinatario.objects.get(id=id_etiq)
        id_remetente = etiqueta.id_remetente        
        etiqueta.delete()        
    except Destinatario.DoesNotExist:        
        raise Http404("id não existe")
    
    try:
        remetente = Remetente.objects.get(id=id_remetente)
        remetente.delete()
    except Remetente.DoesNotExist:
        pass
    
    return HttpResponseRedirect('/')
    

def create_etiq(request):

    count_enviados = len(Destinatario.objects.exclude(data_gerado=None))
    count_pendentes = 0

    try:
        count_pendentes = len(Destinatario.objects.filter(data_gerado=None))
    except Destinatario.DoesNotExist:
        pass

    if request.method == 'POST':        
        form = DestinatarioForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    
    else:
        form = DestinatarioForm()
    
    return render(request, 'etiq_form.html', {
        'form': form,
        'title': 'Adicionar Destinatário',
        'count_enviados': count_enviados,
        'count_pendentes': count_pendentes,
    })

class DestinatarioUpdateView(UpdateView):
    model = Destinatario
    template_name = 'etiq_form.html'
    form_class = DestinatarioForm
    #success_url = '/detalhes/{}'.format(pk)
    success_url = '/'

def pdf_gen(request, id_etiq):

    destinatario = None
    try:
        destinatario = Destinatario.objects.get(id=id_etiq)
    except Destinatario.DoesNotExist:        
        raise Http404("id não existe")

    remetente = None
    try:
        remetente = Remetente.objects.get(id=destinatario.id_remetente)
    except Remetente.DoesNotExist:    
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

    linhas_destinatario = [
        ['DESTINATÁRIO'],
        ['Nome: '+destinatario.nome],
        ['Função: '+destinatario.funcao],
        ['Endereco: '+destinatario.endereco],
        ['Orgão: '+destinatario.orgao],
        ['Email: '+destinatario.email],
    ]
    linhas_remetente= [
        ['REMETENTE'],
        ['Nome: '+remetente.nome],
        ['Função: '+remetente.funcao],
        ['Endereco: '+remetente.endereco],
        ['Orgão: '+remetente.orgao],
        ['Email: '+remetente.email],
    ]

    buffer = create_pdf_buffer(linhas_remetente, linhas_destinatario, title)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    if destinatario.data_gerado == None:
        destinatario.data_gerado = timezone.now()
        destinatario.save()

    return response

def create_pdf_buffer(remetente, destinatario, title):
    # Sample platypus document
    # From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.units import inch
    from reportlab.lib.pagesizes import A4

    width, height = A4

    PAGE_WIDTH, PAGE_HEIGHT = defaultPageSize

    styles = getSampleStyleSheet()

    ############
    def editCanvas(canvas, doc):
        canvas.saveState()
        canvas.setTitle(title)
        canvas.restoreState()

    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    
    Story = []
    
    t=Table(destinatario,[width-2*inch], len(destinatario)*[0.4*inch])
    
    t.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(0,0),colors.gray),
            ('TEXTCOLOR',(0,0),(0,0),colors.white),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
    )

    Story.append(t)

    Story.append(Spacer(1,0.5*inch))    

    t=Table(remetente,[width-2*inch], len(destinatario)*[0.4*inch])
    
    t.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(0,0),colors.gray),
            ('TEXTCOLOR',(0,0),(0,0),colors.white),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
    )

    Story.append(t)
    
    doc.build(Story, onFirstPage=editCanvas)
    
    return buffer


def erro(request):
    return render(request, 'erro.html', {
        'teste': 'teste'
    })