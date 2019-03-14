from django.forms import ModelForm
from .models import Destinatario, Remetente

class RemetenteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RemetenteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    class Meta:
        model = Remetente
        fields = ['nome', 'funcao', 'email', 'orgao', 'endereco']

class DestinatarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DestinatarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    class Meta:
        model = Destinatario
        fields = ['nome', 'funcao', 'email', 'orgao', 'endereco']
