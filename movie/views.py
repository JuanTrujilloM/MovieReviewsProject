import matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64

from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie

# Define views for the movie app
def home(request):
    
    # Handle search functionality
    # If a search term is provided, filter movies by title
    searchItem = request.GET.get('searchMovie')
    if searchItem:
        movies = Movie.objects.filter(title__icontains=searchItem)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchItem, 'movies': movies, 'name': 'Juan Esteban Trujillo Montes'})

# Define a view for the about page
def about(request):
    return render(request, 'about.html')

def signup(request):
    email =request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')
    all_movies = Movie.objects.all()

    # --- Gráfica por año ---
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    # --- Gráfica por género ---
    genre_counts = {}
    for movie in all_movies:
        first_genre = movie.genre.split(',')[0].strip() if movie.genre else "None"
        if first_genre in genre_counts:
            genre_counts[first_genre] += 1
        else:
            genre_counts[first_genre] = 1

    bar_positions = range(len(genre_counts))
    plt.bar(bar_positions, genre_counts.values(), width=bar_width, align='center')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, genre_counts.keys(), rotation=45)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic2 = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    # Renderizar ambas gráficas en el mismo template
    return render(request, 'statistics.html', {
        'graphic': graphic,
        'graphic2': graphic2
    })