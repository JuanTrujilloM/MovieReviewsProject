from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

# Create your views here.

def home(request):
    
    searchItem = request.GET.get('searchMovie')
    if searchItem:
        movies = Movie.objects.filter(title__icontains=searchItem)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchItem, 'movies': movies, 'name': 'Juan Esteban Trujillo Montes'})

def about(request):
    return render(request, 'about.html')