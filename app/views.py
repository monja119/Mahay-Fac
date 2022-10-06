from django.shortcuts import render
from django.http import HttpResponse
from django.http import request


def auth(request):
    msg = 'ok '
    return render(request, 'base.html', locals())
