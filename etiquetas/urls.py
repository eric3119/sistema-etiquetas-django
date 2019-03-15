from django.urls import path
from .views import get_etiq, create_etiq, update_etiq, delete_etiq, pdf_gen, envios, pendentes, erro
from .views import DestinatariosView, DestinatarioDetailView

urlpatterns = [
    path('', DestinatariosView.as_view(), name='home'),
    path('detalhes/<int:pk>/', DestinatarioDetailView.as_view(), name='detalhes'),
    path('envios/', envios, name='envios'),
    path('pendentes/', pendentes, name='pendentes'),
    path('create/', create_etiq, name='criar'),
    path('update/<int:id_etiq>/', update_etiq, name='atualizar'),
    path('delete/<int:id_etiq>/', delete_etiq, name='deletar'),
    path('pdf/<int:id_etiq>', pdf_gen, name='gerar_pdf'),
    path('erro', erro, name='erro'),
]
