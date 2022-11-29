from django.db import models

gender_choice = [
    ('male', 'Male'),
    ('female', 'Female'),
]


class User(models.Model):
    # about
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture = models.FileField(upload_to='static/media/images/user/')
    gender = models.CharField(max_length=6, choices=gender_choice, default='male')
    # company
    company = models.CharField(max_length=50)
    function = models.CharField(max_length=50)

    # contact
    address = models.CharField(max_length=50)
    tel = models.IntegerField(max_length=15)
    mail = models.EmailField(max_length=50)

    # pass
    password = models.CharField(max_length=200)
    repeate = models.CharField(max_length=200)


class Client(models.Model):
    full_name = models.CharField(max_length=50)
    company_id = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    tel = models.IntegerField(max_length=50)
    mail = models.EmailField(max_length=50)


class Company(models.Model):
    # about
    name = models.CharField(max_length=50)
    picture = models.FileField(upload_to='static/media/images/company/')
    status = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    sector = models.CharField(max_length=50)
    creating_date = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    tel = models.IntegerField()

    # not required
    website = models.CharField(max_length=50)
    salary_number = models.IntegerField(max_length=15)

    #
    author = models.IntegerField(null=True)


class Invoice(models.Model):
    company = models.IntegerField()
    destination = models.CharField(max_length=50)
    field_number = models.IntegerField()
    item = models.TextField()
    quantity = models.CharField(max_length=100)
    unite_price = models.CharField(max_length=50)
    tax = models.IntegerField()
    date = models.CharField(max_length=12)
    number = models.IntegerField(default=1)
    unity = models.CharField(max_length=10)
