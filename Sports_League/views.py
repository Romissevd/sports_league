from django.shortcuts import render
from django.http import HttpResponse


def index(request):

    return render(request, 'index.html')

def contacts(request):

    return render(request, 'contacts.html')

def abouts(request):

    return render(request, 'abouts.html')