from django.urls import path
from .views import create_etiq, delete_etiq, pdf_gen, envios, pendentes, erro
from .views import DestinatariosView, DestinatarioDetailView, DestinatarioUpdateView

urlpatterns = [
    path('', DestinatariosView.as_view(), name='home'),
    path('detalhes/<int:pk>/', DestinatarioDetailView.as_view(), name='detalhes'),
    path('envios/', envios, name='envios'),
    path('pendentes/', pendentes, name='pendentes'),
    path('create/', create_etiq, name='criar'),
    path('update/<int:pk>/', DestinatarioUpdateView.as_view(), name='atualizar'),
    path('delete/<int:id_etiq>/', delete_etiq, name='deletar'),
    path('pdf/<int:id_etiq>', pdf_gen, name='gerar_pdf'),
    path('erro', erro, name='erro'),
]
