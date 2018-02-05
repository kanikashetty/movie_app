from django.conf.urls import url, include
from .views import Movie_List, UpdateDeleteMovie, SearchMovie

urlpatterns = [
	url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')), 
	url(r'^movieList/$', Movie_List.as_view(), name="ListMovies"),
	url(r'^movieList/(?P<title>.*)$',UpdateDeleteMovie.as_view(), name="UpdateDeleteMovies"),
	url(r'^searchMovie/$',SearchMovie.as_view(), name="SearchMovie")
	
	]