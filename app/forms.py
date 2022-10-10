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


class NewClientForm(forms.Form):
    full_name = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=[('male', 'male'), ('female', 'female')], widget=forms.RadioSelect)

    company = forms.CharField(max_length=50)

    mail = forms.EmailField(max_length=50)


class Authentificaton(forms.Form):
    Email = forms.EmailField(max_length=50)
    Password = forms.CharField(widget=forms.PasswordInput, required=True)


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


class CreateInvoice(forms.Form):
    date = forms.DateField(input_formats=None)

    # to
    destinataire = forms.CharField(max_length=80)