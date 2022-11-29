import os
from app.exporter import exporter
from app.models import User, Company, Client, Invoice
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from app.forms import NewUserForm, NewClientForm, Authentificaton, CreateCompany
from django.contrib.auth.hashers import make_password, check_password
import datetime


def session_check(request):
    session = None
    try:
        session = request.session['id']
    except KeyError:
        session = None
    return session


def session_set(request, id):
    try:
        request.session['id'] = id
        return 0
    except:
        return -1

def session_del(request):
    del request.session['id']
    return 0


def home(request):
    if session_check(request) is not None:
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

        # picture
        user_picture = str(user.picture).split('/')[-1]
        return redirect(profile)
    else:
        return render(request, 'tab/home.html', locals())


# forms view
def new_user(request):
    form = NewUserForm(request.POST, request.FILES)
    if form.is_valid():
        user = User()
        msg, error_msg = '', ''
        # auth
        mail, password, repeate = form.cleaned_data['mail'], form.cleaned_data['password'], form.cleaned_data['repeate']

        picture = form.cleaned_data['picture']
        content_type = picture.content_type

        # verification si les deux mots de passe sont les même
        if password != repeate:
            error_msg = 'les deux mots de passe ne sont pas les même'
            return render(request, 'authentification/register.html', locals())
        elif 'image' not in content_type:
            error_msg = 'Type d\'image non supporté '
            return render(request, 'authentification/register.html', locals())
        else:
            # ajout à la base de données

            try:
                User.objects.get(mail=mail)
                error_msg = 'Email déjà utilisé par un autre utilisateur'
                form = NewUserForm()
                context = {
                    'form': form
                }
                return render(request, 'authentification/register.html', locals())
            except User.DoesNotExist:
                # about
                form.save()
                user.first_name, user.last_name = form.cleaned_data['first_name'], form.cleaned_data['last_name']
                user.gender = form.cleaned_data['gender']
                # company
                user.company = form.cleaned_data['company']
                user.function = form.cleaned_data['function']

                # contact
                user.address = form.cleaned_data['address']
                user.tel = form.cleaned_data['tel']
                user.mail = form.cleaned_data['mail']

                # managing profile picture
                path_to_picture = 'app/static/media/images/user'
                file_full_name = str(picture)
                file_name = file_full_name.split('.')[:-1]
                file_type = file_full_name.split('.')[-1]
                old_name = '{}/{}'.format(path_to_picture, picture)
                new_name = '{}/{}.{}'.format(path_to_picture, user.mail, file_type)
                os.rename(old_name, new_name)

                user.picture = new_name
                user.password = make_password(password, None, 'default')

                user.save()

                return redirect(auth)


    else:
        form = NewUserForm()
        context = {
            'form': form
        }
        return render(request, 'authentification/register.html', locals())


# authentifiaction
def auth(request):
    if session_check(request) is not None:
        session_id = session_check(request)
        return redirect(profile)
    else:
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
                    request.session['id'] = session_id = user.id
                    # selecting from db
                    user = User.objects.get(id=session_id)
                    first_name = user.first_name
                    last_name = user.last_name
                    # picture
                    user_picture = str(user.picture).split('/')[-1]
                    return redirect(profile)
                else:
                    msg = 'Wrong password'
                    return render(request, 'authentification/auth.html', locals())

            except User.DoesNotExist:
                msg = 'Identifiant inconnu'

                return render(request, 'authentification/auth.html', locals())

        else:
            auth = Authentificaton()

            return render(request, 'authentification/auth.html', locals())


def profile(request):
    # session is set ?
    if  session_check(request) is not None:
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

        # picture
        user_picture = str(user.picture).split('/')[-1]

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

    else:
        return redirect(auth)


def my_company(request):
    try:
        session_id = request.session['id']
        user = request.session['id']
        user = User.objects.get(id=user)
        user_picture = str(user.picture).split('/')[-1]
    except:
        return redirect('authentification')
    companies = 'None'
    # checking companies
    try:
        if request.GET:
            if 'update' in request.GET:
                id = request.GET['update']
                company = data = Company.objects.get(id=id)
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

        else:
            company = Company.objects.filter(author=session_id).order_by('id').reverse()
            companies = company
    except Company.DoesNotExist:
        pass
    return render(request, 'tab/my_company.html', locals())


def create_company(request):
    session_id = request.session['id']
    form = CreateCompany(request.POST, request.FILES)
    try:
        if form.is_valid():
            picture = form.cleaned_data['picture']
            content_type = picture.content_type

            if 'image' not in content_type:
                error_msg = 'Type d\'image non supporté '
                return render(request, 'creation/company.html', locals())
            else:
                company = Company()
                form.save()
                company.name = form.cleaned_data['name']
                company.status = form.cleaned_data['status']
                company.number = form.cleaned_data['number']
                company.sector = form.cleaned_data['sector']
                company.creating_date = form.cleaned_data['creating_date']
                company.address = form.cleaned_data['address']
                company.mail = form.cleaned_data['mail']
                company.tel = form.cleaned_data['tel']
                company.website = form.cleaned_data['website']
                company.salary_number = form.cleaned_data['salary_number']

                # managing profile picture
                path_to_picture = 'app/static/media/images/company'
                file_full_name = str(picture)
                file_name = file_full_name.split('.')[:-1]
                file_type = file_full_name.split('.')[-1]
                old_name = '{}/{}'.format(path_to_picture, picture)
                new_name = '{}/{}.{}'.format(path_to_picture, company.mail, file_type)
                os.rename(old_name, new_name)

                company.picture = new_name
                company.author = session_id
                company.save()
                return redirect(my_company)
        else:
            form = CreateCompany()
            user = User.objects.get(id=session_check(request))
            user_picture = str(user.picture).split('/')[-1]
            return render(request, 'creation/company.html', locals())
    except KeyError:
        return redirect(auth)


def create_invoice(request):
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
        if request.GET:
            if 'company' in request.GET:
                company = data = Company.objects.get(id=int(request.GET['company']))
                company_id = request.GET['company']
                user = User.objects.get(id=company.author)
                user_picture = str(user.picture).split('/')[-1]
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
    if request.method == 'POST':
        client = Client()
        client.full_name = request.POST['full_name']
        client.address = request.POST['address']
        client.tel = request.POST['tel']
        client.mail = request.POST['email']
        client.company_id = request.POST['company_id']
        client.save()
        print(str(request.POST['company_id']))
        url = 'http://localhost:8000/check/?clients={}'.format(str(request.POST['company_id']))
        return redirect(url)

    else:
        company = data = Company.objects.get(id=int(request.GET['company']))
        user = User.objects.get(id=company.author)
        user_picture = str(user.picture).split('/')[-1]
        return render(request, 'creation/client.html', locals())


def check(request, arg):
    url = request.get_full_path()
    arg = url.split('?')[1]
    view = arg.split('=')[0]

    if request.method == 'GET':
        try:
            if 'company' in request.GET:
                data = company = eval('{}'.format(str(view).capitalize())).objects.get(id=request.GET['company'])
                picture = str(data.picture).split('/')[-1]
                user = User.objects.get(id=data.author)
                user_picture = str(user.picture).split('/')[-1]
                return render(request, 'check/company.html', locals())

            if 'clients' in request.GET:
                company = data = Company.objects.get(id=request.GET['clients'])
                clients = Client.objects.filter(company_id=company.id).order_by('full_name')
                user = User.objects.get(id=company.author)
                user_picture = str(user.picture).split('/')[-1]

                size = len(clients)
                return render(request, 'check/clients.html', locals())

            if 'client' in request.GET:
                client = Client.objects.get(id=request.GET['client'])
                company = data = Company.objects.get(id=client.company_id)
                user = User.objects.get(id=company.author)
                user_picture = str(user.picture).split('/')[-1]


                return render(request, 'check/client.html', locals())

            if 'invoices' in request.GET:
                company = data = Company.objects.get(id=int(request.GET['invoices']))
                invoices = Invoice.objects.filter(company=int(company.id))
                user = User.objects.get(id=company.author)
                user_picture = str(user.picture).split('/')[-1]

                size = len(invoices)
                return render(request, 'check/invoices.html', locals())

            if 'invoice' in request.GET:
                invoice = Invoice.objects.get(id=int(request.GET['invoice']))
                company = data = Company.objects.get(id=int(invoice.company))
                user = User.objects.get(id=company.author)
                picture = str(data.picture).split('/')[-1]
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
        except:
            return HttpResponse('Désolé, une erreur s\'est reproduite')


def remove(request, arg):
    msg = ''
    if request.GET:
        if 'client' in request.GET:
            client = Client.objects.get(id=request.GET['client'])
            client.delete()
            msg = 'Client supprimé avec succès'
            return HttpResponse("""
                    <p> client suprimé avec succés </p><br>
                    <a href="http://localhost:8000/check/?clients={}">
                    <input type="button" value="Mes clients">
                </a>
                """.format(request.GET['company']))

        if 'company' in request.GET:
            company = Company.objects.get(id=request.GET['client'])
            company.delete()
            return redirect('http://localhost:8000/company')


def search(request):
    if request.method == 'GET':
        query = request.GET['q']

        return render(request, 'search.html', locals())
    else:
        return HttpResponse("Une erreur s'est produite !")


def export(request, id):
    if request.method == 'GET':
        try:
            invoice_id = request.GET.get('invoice')
            pdf = exporter(invoice_id)
            # downloading pdf file
            return FileResponse(open(pdf, 'rb'), as_attachment=True)

        except Invoice.DoesNotExist:
            return 'Désole, Facture non identifiable'

    else:
        return HttpResponse("Une Erreur s'est reproduite ")
