from django.shortcuts import render, reverse
from .models import Destinatario, Remetente
from .forms import DestinatarioForm, RemetenteForm

from django.http import HttpResponse, HttpResponseRedirect, Http404

from .criar_pdf import create_pdf_buffer

from django.utils import timezone
import pytz

import logging
logger = logging.getLogger(__name__)

from django.views.generic import (ListView, DetailView, UpdateView,
                                    CreateView, DeleteView, View)

from django.contrib.auth import authenticate, login, logout

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
        
        context['title'] = 'Etiquetas'

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count_enviados'] = len(Destinatario.objects.exclude(data_gerado=None))         
        try:
            context['count_pendentes'] = len(Destinatario.objects.filter(data_gerado=None))
        except Destinatario.DoesNotExist:
            context['count_pendentes'] = 0
        
        context['title'] = 'Detalhes'

        return context
    

class DestinatarioDelete(DeleteView):
    model=Destinatario
    template_name='destinatario_confirm_delete.html'
    success_url='/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        remetente_id = self.object.remetente_id   
        self.object.delete()
        try:
            remetente = Remetente.objects.get(id=remetente_id)
            remetente.delete()
        except Remetente.DoesNotExist:
            pass
        return HttpResponseRedirect(success_url) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count_enviados'] = len(Destinatario.objects.exclude(data_gerado=None))         
        try:
            context['count_pendentes'] = len(Destinatario.objects.filter(data_gerado=None))
        except Destinatario.DoesNotExist:
            context['count_pendentes'] = 0
        
        context['title'] = 'Excluir'

        return context

class DestinatarioCreateView(CreateView):
    model = Destinatario
    template_name='etiq_form.html'
    form_class = DestinatarioForm
    success_url='/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count_enviados'] = len(Destinatario.objects.exclude(data_gerado=None))         
        try:
            context['count_pendentes'] = len(Destinatario.objects.filter(data_gerado=None))
        except Destinatario.DoesNotExist:
            context['count_pendentes'] = 0
        
        context['title'] = 'Adicionar'

        return context

class DestinatarioUpdateView(UpdateView):
    model = Destinatario
    template_name = 'etiq_form.html'
    form_class = DestinatarioForm
    def get_success_url(self):
        return reverse('detalhes', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count_enviados'] = len(Destinatario.objects.exclude(data_gerado=None))         
        try:
            context['count_pendentes'] = len(Destinatario.objects.filter(data_gerado=None))
        except Destinatario.DoesNotExist:
            context['count_pendentes'] = 0
        
        context['title'] = 'Editar'

        return context
    
class PDFView(View):
    model=Destinatario

    def get_db_itens_list(self, request, **kwargs):

        destinatario = None
        try:
            destinatario = Destinatario.objects.get(id=kwargs.get('pk'))
        except Destinatario.DoesNotExist:
            raise Http404("id não existe")

        remetente = None
        try:
            remetente = Remetente.objects.get(id=destinatario.remetente_id)
        except Remetente.DoesNotExist:    
            pass
        
        return [destinatario, remetente]
    
    def post(self, request, *args, **kwargs):
        # adicionar remetente
        form = RemetenteForm(request.POST)

        if form.is_valid():
            new_dest = form.save()
            Destinatario.objects.filter(id=kwargs.get('pk')).update(remetente_id=new_dest.pk)
        return HttpResponseRedirect('/pdf/{}'.format(kwargs.get('pk')))
    
    def get(self, request, *args, **kwargs):

        destinatario, remetente = self.get_db_itens_list(request, **kwargs)

        if remetente == None:
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

class UserProfileView(DetailView):

    model=Destinatario
    template_name = 'destinatarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count_enviados'] = len(Destinatario.objects.exclude(data_gerado=None))         
        try:
            context['count_pendentes'] = len(Destinatario.objects.filter(data_gerado=None))
        except Destinatario.DoesNotExist:
            context['count_pendentes'] = 0
        
        context['title'] = 'Etiquetas'

        return context
    
    def get_queryset(self):
        queryset = Destinatario.objects.all()

        if self.request.GET.get('type'):
            if self.request.GET.get('type') == 'enviados':
                queryset = queryset.exclude(data_gerado=None)
            elif self.request.GET.get('type') == 'pendentes':
                queryset = queryset.filter(data_gerado=None)  
        
        return queryset