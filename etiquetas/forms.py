from django.forms import ModelForm
from .models import Destinatario, Rementente

class EtiqForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EtiqForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    class Meta:
        model = Destinatario
        fields = ['nome', 'funcao', 'email', 'orgao', 'endereco']

class RemententeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RemententeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    class Meta:
        model = Rementente
        fields = ['nome', 'funcao', 'email', 'orgao', 'endereco']

class DestinatarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DestinatarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    class Meta:
        model = Destinatario
        fields = ['nome', 'funcao', 'email', 'orgao', 'endereco']
