from django.shortcuts import render, reverse
from .models import Destinatario, Endereco, Orgao, UserProfile
from .forms import DestinatarioForm, EnderecoForm, OrgaoForm, UserProfileForm

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
    
    def get_success_url(self):
        return reverse('inicio')

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
    template_name='etiq_form.html'
    form_class = EnderecoForm
        
    def get_success_url(self):
        return reverse('inicio')    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Adicionar Endereco'

        return context
    
    def form_valid(self, form):        
        
        form.instance.user = self.request.user
        
        self.object = form.save()
        return super().form_valid(form)

class OrgaoCreateView(LoginRequiredMixin, CreateView):
    model = Orgao
    template_name='etiq_form.html'
    form_class = OrgaoForm

    def get_success_url(self):
        return reverse('inicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Adicionar Orgão'

        return context
    
    def form_valid(self, form):        
        
        form.instance.user = self.request.user
        
        self.object = form.save()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())


class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    template_name='etiq_form.html'
    form_class = UserProfileForm
    
    def get_success_url(self):
        return reverse('inicio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Adicionar Informações'

        return context
    
    def form_valid(self, form):        
        
        form.instance.user = self.request.user
        
        self.object = form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())


class DestinatarioCreateView(LoginRequiredMixin, CreateView):
    model = Destinatario
    template_name='etiq_form.html'
    form_class = DestinatarioForm
    
    def get_success_url(self):
        return reverse('inicio')

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
        return reverse('detalhes_destinatario', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Destinatario.objects.filter(remetente=self.request.user)
        enviados = total.exclude(data_gerado=None)
        context['count_enviados'] = len(enviados)
        context['count_pendentes'] = len(total)-context['count_enviados']
        
        context['title'] = 'Editar Destinatario'

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(remetente=self.request.user)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())
    
class PDFView(LoginRequiredMixin, View):    

    def get_destinatario(self, request, **kwargs):
        
        id_destinatario = kwargs.get('pk')
        
        destinatario = None
        try:
            destinatario = Destinatario.objects.get(id=id_destinatario, remetente=self.request.user)
        except Destinatario.DoesNotExist:
            raise Http404("id não existe")
        
        return destinatario
    
    def get(self, request, *args, **kwargs):

        destinatario = self.get_destinatario(request, **kwargs)
        user = self.request.user._wrapped if hasattr(self.request.user,'_wrapped') else self.request.user
        user_info = UserProfile.objects.get(user_id=user.id)

        title = 'etiqueta{}'.format(destinatario.id)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+title+'.pdf"'

        linhas_destinatario = [
            ['DESTINATÁRIO'],
            ['Nome: '+destinatario.nome],
            ['Função: '+destinatario.funcao],            
            ['Orgão: '+destinatario.orgao.nome],
            ['Endereco: '+destinatario.orgao.endereco.__str__()],
            ['Email: '+destinatario.email],
        ]
        linhas_remetente= [
            ['REMETENTE'],            
            ['Nome: '+user.username],
            ['Função: '+user_info.funcao],
            ['Endereco: '+user_info.orgao.endereco.__str__()],
            ['Orgão: '+user_info.orgao.__str__()],
            ['Email: '+user.email],
        ]

        buffer = create_pdf_buffer(linhas_remetente, linhas_destinatario, title)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        if destinatario.data_gerado == None:
            destinatario.data_gerado = timezone.now()
            destinatario.save()

        return response