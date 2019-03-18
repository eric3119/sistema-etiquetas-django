from django.urls import path, re_path
from .views import pdf_gen
from .views import (DestinatariosView, DestinatarioDetailView, DestinatarioUpdateView,
                    DestinatarioCreateView, DestinatarioDelete)

urlpatterns = [    
    path('', DestinatariosView.as_view(), name='home'),
    path('detalhes/<int:pk>/', DestinatarioDetailView.as_view(), name='detalhes'),
    path('create/', DestinatarioCreateView.as_view(), name='criar'),
    path('update/<int:pk>/', DestinatarioUpdateView.as_view(), name='atualizar'),
    path('delete/<int:pk>/', DestinatarioDelete.as_view(), name='deletar'),
    path('pdf/<int:id_etiq>', pdf_gen, name='gerar_pdf'),
]
