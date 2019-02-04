from django.shortcuts import render
from django.http import HttpResponse


def index(request):

    return render(request, 'index.html')

def news(request):

    return render(request, 'news.html')

def contacts(request):

    return render(request, 'contacts.html')

def abouts(request):

    return render(request, 'abouts.html')