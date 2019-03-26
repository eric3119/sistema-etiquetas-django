from django.urls import path, include
from .views import (DestinatariosView, DestinatarioDetailView, DestinatarioUpdateView,
                    DestinatarioCreateView, DestinatarioDelete, PDFView)
from django.contrib.auth.views import LoginView

urlpatterns = [    
    path('', DestinatariosView.as_view(), name='home'),
    path('detalhes/<int:pk>/', DestinatarioDetailView.as_view(), name='detalhes'),
    path('create/', DestinatarioCreateView.as_view(), name='criar'),
    path('update/<int:pk>/', DestinatarioUpdateView.as_view(), name='atualizar'),
    path('delete/<int:pk>/', DestinatarioDelete.as_view(), name='deletar'),
    path('pdf/<int:pk>', PDFView.as_view(), name='gerar_pdf'),
    path('accounts/', include('django.contrib.auth.urls')),
]
