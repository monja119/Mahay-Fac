from django.db import models


class User(models.Model):
    # about
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6)

    # company
    company = models.CharField(max_length=50)
    function = models.CharField(max_length=50)

    # contact
    address = models.CharField(max_length=50)
    tel = models.IntegerField(max_length=15)
    mail = models.EmailField(max_length=50)

    # pass
    password = models.CharField(max_length=200)


class Client(models.Model):
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6)
    company = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    company_id = models.IntegerField()

class Company(models.Model):
    # about
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    number = models.CharField(max_length=6)
    sector = models.CharField(max_length=50)
    creating_date = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    tel = models.IntegerField()

    # not required
    website = models.CharField(max_length=50)
    salary_number = models.IntegerField(max_length=15)

    #
    author = models.IntegerField()


class Invoice(models.Model):
    company = models.IntegerField()
    destination = models.CharField(max_length=50)
    field_number = models.IntegerField()
    item = models.TextField()
    quantity = models.CharField(max_length=100)
    unite_price = models.CharField(max_length=50)
    tax = models.IntegerField()

