from rest_framework import serializers
from rest_framework import exceptions
from .models import MovieList
import logging

logger = logging.getLogger(__name__)

class MovieSerializer(serializers.ModelSerializer):
	"serializer to convert the data to json and reverse for MovieList "

	owner = serializers.ReadOnlyField(source="owner.username")
	
	class Meta:
		model = MovieList
		fields = '__all__'
		
	# def to_representation(self, inst, ance):
	# 	ret = super(MovieSerializer, self).to_representation(instance)
	# 	print("ret",ret)
	# 	ret['99popularity'] = ret['popularity_99']
	# 	del ret['popularity_99']
	# 	return ret

	def to_internal_value(self, data):
		if '99popularity' in data.keys():
			data['popularity_99'] = data['99popularity']
			del data['99popularity']
		print('internal', data)

		if not data['popularity_99']:
			logger.error('popularity_99 : This field is required.')
			raise exceptions.ValidationError({
                                'popularity_99': 'This field is required.'
                                })
		
		elif float(data['popularity_99']) < 0 or float(data['popularity_99']) > 100:
			logger.error('popularity_99 : This field should be floating value between 0 to 100.')
			raise exceptions.ValidationError({
                                'popularity_99': 'This field should be floating value between 0 to 100.'
                                })

		elif not data['name']:
			logger.error('name : This field is required.')
			raise exceptions.ValidationError({
                                'name': 'This field is required.'
                                })

		elif not data['director']:
			logger.error('director : This field is required.')
			raise exceptions.ValidationError({
                                'director': 'This field is required.'
                                })

		elif not data['genre']:
			logger.error('genre :This field is required.')
			raise exceptions.ValidationError({
                                'genre: This field is required.'
                                })

		elif not data['imdb_score']:
			logger.error('imdb_score : This field is required.')
			raise exceptions.ValidationError({
                                'imdb_score': 'This field is required.'
                                })

		elif float(data['imdb_score']) > 10.0 or float(data['imdb_score']) < 0:
			logger.error('imdb_score : This field should floating value be between 0 to 10.')
			raise exceptions.ValidationError({
                                'imdb_score':'This field should floating value be between 0 to 10.'
                                })
		return data
	
	def create(self,validated_data):
		print("validated_data",validated_data)
		user_data = self.context['request'].user
		
		
		
		create_movie = MovieList(
							popularity_99=validated_data['popularity_99'],
							name=validated_data['name'],
                            director=validated_data['director'],
                            genre=validated_data['genre'],
                            imdb_score=validated_data['imdb_score'],
                            owner = user_data
                            )
		create_movie.save()
		return create_movie
	def update(self, instance, validated_data):
		print('update ',validated_data)
		instance.name = validated_data.get('name', instance.name)
		instance.popularity_99 = validated_data.get('popularity_99',instance.popularity_99)
		instance.imdb_score = validated_data.get('imdb_score',instance.imdb_score)
		instance.director = validated_data.get('director', instance.director)
		instance.genre = validated_data.get('genre', instance.genre)
		instance.save()
		return instance