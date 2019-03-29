from django.forms import ModelForm, ModelChoiceField
from .models import Destinatario, Endereco, Orgao, UserProfile

class DestinatarioForm(ModelForm):    
    
    def __init__(self, user, *args, **kwargs):
        super(DestinatarioForm, self).__init__(*args, **kwargs)    

        self.fields['orgao'].queryset = Orgao.objects.filter(user=user)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    
    class Meta:
        model = Destinatario
        fields = ['nome','funcao','email','orgao']

class OrgaoForm(ModelForm):    
    
    def __init__(self, user, *args, **kwargs):
        super(OrgaoForm, self).__init__(*args, **kwargs)
        
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    
    class Meta:
        model = Orgao
        fields = ['nome', 'endereco']


class EnderecoForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(EnderecoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'cidade', 'cep', 'estado']

class UserProfileForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)  
        self.fields['orgao'].queryset = Orgao.objects.filter(user=user)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    
    class Meta:
        model = UserProfile
        fields=['funcao','orgao']