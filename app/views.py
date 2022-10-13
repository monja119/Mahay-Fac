from app.models import User, Company, Client, Invoice
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import request
from app.forms import NewUserForm, NewClientForm, Authentificaton, CreateCompany
from django.contrib.auth.hashers import make_password, check_password
import datetime


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
        mail = auth.cleaned_data['email']
        password = auth.cleaned_data['password']
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
        session_id = request.session['id']
        msg = 'ok'
        return render(request, 'tab/home.html', locals())

    except KeyError:
        return redirect(auth)


def profile(request):
    # session is set ?
    try:
        session_id = request.session['id']

        # selecting from db
        user = User.objects.get(id=session_id)
        first_name = user.first_name
        last_name = user.last_name
        user_gender = user.gender

        user_company = user.company
        user_function = user.function

        user_address = user.address
        user_tel = user.tel
        user_mail = user.mail

        # if wanted to modify
        if request.GET:
            if 'update' in request.GET:
                return render(request, 'tab/profile_update.html', locals())

            elif 'logout' in request.GET:
                del request.session['id']
                return redirect('authentification')
            else:
                return render(request, 'tab/profile.html', locals())

        elif request.POST:
            user = User.objects.get(id=session_id)
            # about
            user.first_name, user.last_name = first_name, last_name = request.POST['first_name'], request.POST[
                'last_name']

            # company
            user.company = user_company = request.POST['company']
            user.function = user_function = request.POST['function']

            # contact
            user.address = user_address = request.POST['address']
            user.tel = user_tel = request.POST['tel']

            if user_mail != request.POST['mail']:
                user.mail = user_mail = request.POST['mail']
                try:
                    error_msg = 'Mail déjà utilisé'
                    verify = User.objects.get(mail=user_mail)
                except User.DoesNotExist:
                    user.save()
            else:
                user.save()
            return render(request, 'tab/profile.html', locals())
        else:
            return render(request, 'tab/profile.html', locals())

    except KeyError:
        return redirect(auth)


def my_company(request):
    try:
        session_id = request.session['id']
        companies = 'None'
        # checking companies
        try:
            if request.GET:
                if 'update' in request.GET:
                    id = request.GET['update']
                    company = Company.objects.get(id=id)
                    return render(request, 'tab/my_company_update.html', locals())
            elif request.POST:
                company = Company.objects.get(id=request.POST['id'])
                company.name = request.POST['name']
                company.status = request.POST['status']
                company.number = request.POST['number']
                company.sector = request.POST['sector']
                company.creating_date = request.POST['creating_date']
                company.address = request.POST['address']
                company.mail = request.POST['mail']
                company.tel = request.POST['tel']
                company.website = request.POST['website']
                company.salary_number = request.POST['salary_number']

                company.save()
                return redirect('http://localhost:8000/check/?company={}'.format(request.POST['id']))

                company.save()
                return redirect('ok')
            else:
                company = Company.objects.filter(author=session_id).order_by('id').reverse()
                companies = company
        except Company.DoesNotExist:
            pass
        return render(request, 'tab/my_company.html', locals())
    except KeyError:
        return redirect(auth)


def create_company(request):
    try:
        session_id = request.session['id']
        form = CreateCompany(request.POST)
        if form.is_valid():
            company = Company()
            company.name = form.cleaned_data['nom']
            company.status = form.cleaned_data['status_juridique']
            company.number = form.cleaned_data['numero_SIRET_ou_SIREN_et_code_NAF']
            company.sector = form.cleaned_data['secteur']
            company.creating_date = form.cleaned_data['date_de_creation']
            company.address = form.cleaned_data['adresse']
            company.mail = form.cleaned_data['email']
            company.tel = form.cleaned_data['tel']
            company.website = form.cleaned_data['siteweb']
            company.salary_number = form.cleaned_data['nombre_de_salaries']

            company.author = session_id

            company.save()
            return redirect(my_company)
        else:
            form = CreateCompany()
            return render(request, 'creation/company.html', locals())
    except KeyError:
        return redirect(auth)


def create_invoice(request):
    if request.GET:
        if 'company' in request.GET:
            company_id = request.GET['company']
    if request.POST:
        invoice = Invoice()
        company_id = request.POST['company_id']

        # incrementing invoice number for one client
        try:
            invoice_number = Invoice.objects.get(company=company_id, destination=request.POST['destination'])
            invoice.number += 1
        except Invoice.DoesNotExist:
            invoice.number = 1
        invoice.destination = request.POST['destination']
        invoice.field_number = int(request.POST['number'])
        invoice.company = company_id
        invoice.date = datetime.date.today()
        invoice.unity = str(request.POST['unity']).capitalize()
        # numerous field
        for n in range(1, invoice.field_number + 1):
            if n == 1:
                invoice.item += '{}'.format(request.POST['item{}'.format(n)])
                invoice.quantity += '{}'.format(request.POST['quantity{}'.format(n)])
                invoice.unite_price += '{}'.format(request.POST['unitePrice{}'.format(n)])
            else:
                invoice.item += ', {}'.format(request.POST['item{}'.format(n)])
                invoice.quantity += ', {}'.format(request.POST['quantity{}'.format(n)])
                invoice.unite_price += ', {}'.format(request.POST['unitePrice{}'.format(n)])

        invoice.tax = int(request.POST['tax'])
        invoice.save()
        return redirect('http://localhost:8000/check/?invoice={}'.format(invoice.id))
    else:
        return render(request, 'creation/invoice.html', locals())


def client(request):
    if request.GET:
        if 'update' in request.GET:
            client = Client.objects.get(id=request.GET['update'])
            company = Company.objects.get(id=client.company_id)
            return render(request, 'tab/client_update.html', locals())

    if request.POST:
        client_id = request.POST['client_id']
        company_id = request.POST['company_id']

        client = Client.objects.get(id=client_id)
        client.full_name = request.POST['full_name']
        client.save()
        url = 'http://localhost:8000/check/?client={}'.format(str(request.POST['client_id']))
        return redirect(url)


def create_client(request):
    if 'company' in request.GET:
        company_id = request.GET['company']
    company = ''
    form = NewClientForm(request.GET)
    if form.is_valid():
        client = Client()
        client.full_name = form.cleaned_data['full_name']
        client.gender = form.cleaned_data['gender']
        client.company = form.cleaned_data['company']
        client.mail = form.cleaned_data['mail']
        client.company_id = request.GET['company_id']
        client.save()
        url = 'http://localhost:8000/check/?clients={}'.format(str(client.company_id))
        return redirect(url)

    else:
        form = NewClientForm()
        return render(request, 'creation/client.html', locals())


def check(request, arg):
    url = request.get_full_path()
    arg = url.split('?')[1]
    view = arg.split('=')[0]

    if request.method == 'GET':
        if 'company' in request.GET:
            data = eval('{}'.format(str(view).capitalize())).objects.get(id=request.GET['company'])
            return render(request, 'check/company.html', locals())

        if 'clients' in request.GET:
            company = Company.objects.get(id=request.GET['clients'])
            clients = Client.objects.filter(company_id=company.id).order_by('full_name')
            return render(request, 'check/clients.html', locals())

        if 'client' in request.GET:
            client = Client.objects.get(id=request.GET['client'])
            company = Company.objects.get(id=client.company_id)
            return render(request, 'check/client.html', locals())

        if 'invoices' in request.GET:
            company = Company.objects.get(id=int(request.GET['invoices']))
            invoices = Invoice.objects.filter(company=int(company.id))
            return render(request, 'check/invoices.html', locals())

        if 'invoice' in request.GET:
            invoice = Invoice.objects.get(id=int(request.GET['invoice']))
            company = Company.objects.get(id=int(invoice.company))

            items_value = []
            invoice_item = invoice.item.split(', ')
            invoice_quatity = invoice.quantity.split(', ')
            invoice_unite_price = invoice.unite_price.split(', ')
            invoice_total = 0
            for i in range(int(invoice.field_number)):
                sub_total = int(invoice_quatity[i]) * int(invoice_unite_price[i])
                invoice_total += sub_total
                field = """
                    {},{},{} {},{} {}
                """.format(invoice_item[i],
                           invoice_quatity[i],
                           invoice_unite_price[i],
                           invoice.unity,
                           sub_total,
                           invoice.unity)
                items_value.append(field.split(','))

            total = int(invoice_total - ((invoice_total * invoice.tax) / 100))

            return render(request, 'check/invoice.html', locals())


def remove(request, arg):
    msg = 'Erreur'
    if request.GET:
        if 'client' in request.GET and 'company' in request.GET:
            client = Client.objects.get(id=request.GET['client'])
            client.delete()
            msg = 'Client supprimé avec succès'
    return HttpResponse("""
        <p> client suprimé avec succés </p><br>
        <a href="http://localhost:8000/check/?clients={}">
        <input type="button" value="Mes clients">
    </a>
    """.format(request.GET['company']))
