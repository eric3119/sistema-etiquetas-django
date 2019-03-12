from django.urls import path
from .views import home, get_etiq, create_etiq, update_etiq, delete_etiq, pdf_gen, envios

urlpatterns = [
    path('', home, name='home'),
    path('etiqueta/<int:id_etiq>/', get_etiq, name='detalhes'),
    path('envios/', envios, name='envios'),
    path('create/', create_etiq, name='criar'),
    path('update/<int:id_etiq>/', update_etiq, name='atualizar'),
    path('delete/<int:id_etiq>/', delete_etiq, name='deletar'),
    path('pdf/<int:id_etiq>', pdf_gen, name='gerar_pdf'),
]
