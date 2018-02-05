from rest_framework import generics, filters, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import permissions
from  .models import MovieList
from .serializers import MovieSerializer
from django.utils.six import BytesIO

import json
import logging

logger = logging.getLogger(__name__)
# Create your views here.
class Movie_List(generics.ListCreateAPIView):
	"view to add and list the movies"
	try:
	
		serializer_class = MovieSerializer
		queryset = MovieList.objects.all()
		permission_classes = (permissions.IsAuthenticatedOrReadOnly, ) 
		"Only Owner will have permission to add,edit and delete movies"

		def perform_create(self, serializer):
			if serializer.is_valid():
				serializer.save()
			else :
				serializer.is_valid(raise_exception=True)
	except Exception as e:
		logger.error(e)



class UpdateDeleteMovie(generics.RetrieveUpdateDestroyAPIView):
	"Handles updating and deleting of the movies"
	try:
		queryset = MovieList.objects.all()
		serializer_class = MovieSerializer
		permission_classes = (permissions.IsAuthenticated, ) 

		def get(self,request,title):
			print('get', self.request.data)
		
			"Lists all the existing movies"
			queryset = MovieList.objects.filter(name=title)
			serializer = MovieSerializer(queryset, many=True)
			return Response(serializer.data)
		
		def delete(self,request,title):
			print('get', self.request.data)
			"Deletes the movie with requested title"

			MovieList.objects.filter(name=title).delete()
			queryset = self.get_queryset()
			serializer = MovieSerializer(queryset, many=True)
			return Response(serializer.data)
		
		def put(self,request,title):
			print('put', self.request.data)
			data = self.request.data
			"Deletes the movie with requested title"
			# return self.update(request, *args, **kwargs)
			if '99popularity' in data.keys():
				data['popularity_99'] = data['99popularity']
				del data['99popularity']
				print('after replace',data)
			result = MovieSerializer.to_internal_value(self, data)
			if result:
				update_movie = MovieList.objects.update(popularity_99=data['popularity_99'],
									name=data['name'],
		                            director=data['director'],
		                            genre=data['genre'],
		                            imdb_score=data['imdb_score'])
			return update_movie
	except Exception as e:
		logger.exception(e)

class SearchMovie(generics.ListAPIView):
	"search movies using name as filter"
	queryset = MovieList.objects.all()
	serializer_class = MovieSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('^name',)
