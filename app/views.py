from app.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import request
from app.forms import NewUserForm, Authentificaton
from django.contrib.auth.hashers import make_password, check_password


# forms view
def new_user(request):
    form = NewUserForm(request.POST)
    if form.is_valid():
        msg, error_msg = 'register ok', ''

        # auth
        mail, password, repeate = form.cleaned_data['mail'], form.cleaned_data['password'], form.cleaned_data['repeate']

        # verification si les deux mots de passe sont les même
        if password != repeate:
            error_msg = 'les deux mots de passe ne sont pas les même'
            return render(request, 'authentification/register.html', locals())
        else:
            # ajout à la base de données
            user = User()
            try:
                User.objects.get(mail=mail)
                error_msg = 'Email déjà utilisé par un autre utilisateur'
            except User.DoesNotExist:
                # about
                user.first_name, user.last_name = form.cleaned_data['first_name'], form.cleaned_data['last_name']
                user.gender = form.cleaned_data['gender']

                # company
                user.company = form.cleaned_data['company']
                user.function = form.cleaned_data['function']

                # contact
                user.address = form.cleaned_data['address']
                user.tel = form.cleaned_data['tel']
                user.mail = form.cleaned_data['mail']

                user.password = make_password(password, None, 'default')

                user.save()

                return redirect(auth)


    else:
        form = NewUserForm()
        return render(request, 'authentification/register.html', locals())


# authentifiaction
def auth(request):
    auth = Authentificaton(request.POST)
    bolean = False
    if auth.is_valid():
        msg = ''

        # authentification value
        mail = auth.cleaned_data['Email']
        password = auth.cleaned_data['Password']
        try:
            # mail exists ?
            user = User.objects.get(mail=mail)

            # password True ?
            if check_password(password, user.password):
                # valid
                request.session['id'] = user.id
                return redirect(home)
            else:
                msg = 'Wrong password'
                return render(request, 'authentification/auth.html', locals())

        except User.DoesNotExist:
            msg = 'Identifiant inconnu'

            return render(request, 'authentification/auth.html', locals())

    else:
        auth = Authentificaton()

        return render(request, 'authentification/auth.html', locals())

def home(request):
    text = 'Welcome'

    try:
        session = request.session['id']
        msg = 'ok'
        return render(request, 'tab/home.html', locals())
    except KeyError:
        return redirect(auth)

