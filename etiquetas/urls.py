from django.urls import path, include
from .views import (DestinatariosView, DestinatarioDetailView, DestinatarioUpdateView,
                    DestinatarioCreateView, EnderecoCreateView, DestinatarioDelete, OrgaoCreateView,
                    PDFView)
from django.contrib.auth.views import LoginView

urlpatterns = [    
    path('', DestinatariosView.as_view(), name='inicio'),
    path('detalhes/<int:pk>/', DestinatarioDetailView.as_view(), name='detalhes_destinatario'),
    path('add/destinatario/', DestinatarioCreateView.as_view(), name='criar_destinatario'),
    path('add/orgao/', OrgaoCreateView.as_view(), name='criar_orgao'),
    path('add/endereco/', EnderecoCreateView.as_view(), name='criar_endereco'),
    path('update/<int:pk>/', DestinatarioUpdateView.as_view(), name='atualizar_destinatario'),
    path('delete/<int:pk>/', DestinatarioDelete.as_view(), name='deletar_destinatario'),
    path('pdf/<int:pk>/', PDFView.as_view(), name='gerar_pdf'),
    path('accounts/', include('django.contrib.auth.urls')),
]
