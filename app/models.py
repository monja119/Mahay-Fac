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
