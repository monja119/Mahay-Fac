from django import forms


class NewUserForm(forms.Form):
    # about
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=[('male', 'male'), ('female', 'female')], widget=forms.RadioSelect)
    # company
    company = forms.CharField(max_length=50)
    function = forms.CharField(max_length=50)

    # contact
    address = forms.CharField(max_length=50)
    tel = forms.IntegerField()
    mail = forms.EmailField(max_length=50)

    # pass
    password = forms.CharField(max_length=50)
    repeate = forms.CharField(max_length=50)


class Authentificaton(forms.Form):
    Email = forms.EmailField(max_length=50)
    Password = forms.CharField(widget=forms.PasswordInput, required=True)

