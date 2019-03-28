from django.shortcuts import render, reverse
from .models import Destinatario, Endereco
from .forms import DestinatarioForm, EnderecoForm

from django.http import HttpResponse, HttpResponseRedirect, Http404

from .criar_pdf import create_pdf_buffer

from django.utils import timezone
import pytz

import logging
logger = logging.getLogger(__name__)

from django.views.generic import (ListView, DetailView, UpdateView,
                                    CreateView, DeleteView, View)

from django.contrib.auth.mixins import LoginRequiredMixin

class DestinatariosView(LoginRequiredMixin, ListView):

    model=Destinatario
    template_name = 'destinatarios.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Etiquetas'

        return context
    
    def get_queryset(self):
        queryset = Destinatario.objects.filter(remetente=self.request.user).order_by('id')

        if self.request.GET.get('type'):
            if self.request.GET.get('type') == 'enviados':
                queryset = queryset.exclude(data_gerado=None)
            elif self.request.GET.get('type') == 'pendentes':
                queryset = queryset.filter(data_gerado=None)  
        
        return queryset

class DestinatarioDetailView(LoginRequiredMixin, DetailView):
    model=Destinatario
    template_name='etiq_item.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Detalhes'

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(remetente = self.request.user)
    

class DestinatarioDelete(LoginRequiredMixin, DeleteView):
    model=Destinatario
    template_name='destinatario_confirm_delete.html'
    success_url='/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Excluir'

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(remetente = self.request.user)


class EnderecoCreateView(LoginRequiredMixin, CreateView):
    model = Endereco
    template_name='endr_form.html'
    form_class = EnderecoForm
    success_url='/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Adicionar Endereco'

        return context
    
    def form_valid(self, form):        
        form.instance.remetente = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class DestinatarioCreateView(LoginRequiredMixin, CreateView):
    model = Destinatario
    template_name='etiq_form.html'
    form_class = DestinatarioForm
    success_url='/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Adicionar Destinatario'

        return context
    
    def form_valid(self, form):        
        form.instance.remetente = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

class DestinatarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Destinatario
    template_name = 'etiq_form.html'
    form_class = DestinatarioForm
    def get_success_url(self):
        return reverse('detalhes', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Editar'

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(remetente=self.request.user)
    
class PDFView(LoginRequiredMixin, View):
    model=Destinatario

    def get_db_itens_list(self, request, **kwargs):

        destinatario = None
        try:
            destinatario = Destinatario.objects.get(id=kwargs.get('pk'))
        except Destinatario.DoesNotExist:
            raise Http404("id não existe")

        remetente = None
        # try:
        #     remetente = Remetente.objects.get(id=destinatario.remetente_id)
        # except Remetente.DoesNotExist:    
        #     pass
        
        return [destinatario, remetente]
    
    # def post(self, request, *args, **kwargs):
    #     # adicionar remetente
    #     form = RemetenteForm(request.POST)

    #     if form.is_valid():
    #         new_dest = form.save()
    #         Destinatario.objects.filter(id=kwargs.get('pk')).update(remetente_id=new_dest.pk)
    #     return HttpResponseRedirect('/pdf/{}'.format(kwargs.get('pk')))
    
    def get(self, request, *args, **kwargs):

        destinatario, remetente = self.get_db_itens_list(request, **kwargs)

        # if remetente == None:
        #     return render(request, 'etiq_form.html', {
        #         'form': RemetenteForm(),
        #         'title': 'Remetente'
        #     })
        
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