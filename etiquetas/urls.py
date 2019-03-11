from django.urls import path
from .views import home, get_etiq, create_etiq, update_etiq, delete_etiq, pdf_gen, envios

urlpatterns = [
    path('', home),
    path('etiqueta/<int:id_etiq>/', get_etiq),
    path('envios/', envios),
    path('create/', create_etiq),
    path('update/<int:id_etiq>/', update_etiq),
    path('delete/<int:id_etiq>/', delete_etiq),
    path('pdf/<int:id_etiq>', pdf_gen),
]
