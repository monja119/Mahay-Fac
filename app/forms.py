from django.forms import ModelForm
from django import forms
from app.models import User, Company
from django.forms import CharField
from django import forms

class NewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'picture', 'gender'
                  , 'company', 'function', 'address', 'tel', 'mail', 'password', 'repeate']
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'mt-3',
            })
        }
        labels = {
            'first_name': '', 'last_name': '', 'picture': '', 'gender': '', 'company': '', 'function': '',
            'address': '', 'tel': '', 'mail': '', 'password': '', 'repeate': ''
        }

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


class CreateCompany(ModelForm):
    # about
    class Meta:
        model = Company
        fields = [
            'name', 'picture', 'status', 'number', 'sector', 'creating_date', 'address',
            'mail', 'website', 'tel', 'salary_number'
            ]
