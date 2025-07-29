from django.db import models

# Create the Movie model with the required fields
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='movies/images/')
    url = models.URLField(blank=True)