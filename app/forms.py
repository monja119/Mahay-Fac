from django import forms


class NewUserForm(forms):
    # about
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    gender_male = forms.BooleanField(help_text='male')
    gender_female = forms.BooleanField(help_text='female')

    # company
    company = forms.TextInput()
    function = forms.TextInput()

    # contact
    address = forms.TextInput()
    tel = forms.NumberInput()
    mail = forms.EmailInput()

