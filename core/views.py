from django.http import HttpResponse
from django.shortcuts import redirect


# Create your views here.

def home(request):
    return redirect('/admin/')