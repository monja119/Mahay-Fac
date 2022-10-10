from django.forms import ModelForm
from django import forms
from app.models import User


class NewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'picture', 'gender'
                  , 'company', 'function', 'address', 'tel', 'mail', 'password', 'repeate']


class NewClientForm(forms.Form):
    full_name = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=[('male', 'male'), ('female', 'female')], widget=forms.RadioSelect)

    company = forms.CharField(max_length=50)

    mail = forms.EmailField(max_length=50)


class Authentificaton(forms.Form):
    email = forms.EmailField(max_length=50,
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Email',
                                 'class': 'col-8 rounded'
                             }),
                             required=True)

    password = forms.CharField(label="Mot De Passe",
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Mot De Passe',
                                   'class': 'col-8 rounded'
                               }),
                               required=True)


class CreateCompany(forms.Form):
    # about
    nom = forms.CharField(max_length=50)
    status_juridique = forms.CharField(max_length=50)
    numero_SIRET_ou_SIREN_et_code_NAF = forms.CharField(max_length=50)
    secteur = forms.CharField(max_length=50)
    date_de_creation = forms.CharField(max_length=50)
    adresse = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    tel = forms.IntegerField()

    # not required
    siteweb = forms.CharField(max_length=50, required=False)
    nombre_de_salaries = forms.IntegerField(required=False)

