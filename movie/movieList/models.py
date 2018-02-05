from django.db import models

# Create your models here.
class MovieList(models.Model):

#Creates model which lists the Movie 
	owner = models.ForeignKey('auth.User',related_name='Movielist', on_delete=models.CASCADE) 
	" defining admin who can read and write data"
	popularity_99 = models.DecimalField(max_digits=4, decimal_places=2)
	director = models.CharField(max_length=100, null=True)
	genre = models.TextField()
	imdb_score = models.DecimalField(max_digits=4, decimal_places=2)
	name = models.CharField(max_length=100,db_index=True)

