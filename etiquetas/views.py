from django.shortcuts import render, reverse
from .models import Destinatario, Remetente
from .forms import DestinatarioForm, RemetenteForm

from django.http import FileResponse, HttpResponse, HttpResponseRedirect, Http404

from .criar_pdf import create_pdf_buffer

from django.utils import timezone
import pytz

import logging
logger = logging.getLogger(__name__)

from django.views.generic import (TemplateView, ListView, DetailView, 
                                    UpdateView, CreateView, DeleteView)

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
    
    def get_queryset(self):
        queryset = Destinatario.objects.all()

        if self.request.GET.get('type'):
            if self.request.GET.get('type') == 'enviados':
                queryset = queryset.exclude(data_gerado=None)
            elif self.request.GET.get('type') == 'pendentes':
                queryset = queryset.filter(data_gerado=None)  
        
        return queryset

class DestinatarioDetailView(DetailView):
    model=Destinatario
    template_name='etiq_item.html'

class DestinatarioDelete(DeleteView):
    model=Destinatario
    template_name='destinatario_confirm_delete.html'
    success_url='/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        id_remetente = self.object.id_remetente   
        self.object.delete()
        try:
            remetente = Remetente.objects.get(id=id_remetente)
            remetente.delete()
        except Remetente.DoesNotExist:
            pass
        return HttpResponseRedirect(success_url)    

class DestinatarioCreateView(CreateView):
    model = Destinatario
    template_name='etiq_form.html'
    form_class = DestinatarioForm
    success_url='/'

class DestinatarioUpdateView(UpdateView):
    model = Destinatario
    template_name = 'etiq_form.html'
    form_class = DestinatarioForm    
    def get_success_url(self):
        return reverse('detalhes', kwargs={'pk': self.object.pk})
    
# class RemetenteCreateView(CreateView):
#     model = Remetente
#     template_name='etiq_form.html'
#     form_class = RemetenteForm
#     success_url='/pdf/'

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