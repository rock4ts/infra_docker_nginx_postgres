import datetime

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, GenreTitle, Title


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class GenreSlugSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()

    class Meta:
        model = Genre
        fields = ('slug',)


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug', read_only=True)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category',)


class PostTitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug', read_only=True)
    genre = GenreSlugSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'
    
    def validate(self, data):
        if datetime.date.today().year < data['year']:
            raise serializers.ValidationError(
                'Publication year can not be later then current year!'
            )

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genre.objects.get(slug=genre)
            GenreTitle.objects.create(
                genre_id=current_genre, title_id=title
            )
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.category = validated_data.get('category', instance.category)
        if 'genre' in validated_data:
            genres = validated_data.pop('genre')
            lst = []
            for genre in genres:
                current_genre, status = Genre.objects.get_or_create(**genre)
                lst.append(current_genre)
            instance.genre.set(lst)

        instance.save()
        return instance


'''
def to_internal_value(self, data):
        genres = data.get('genre')
        if genres:
            data['genre'] = []
            for genre in genres:
                
                data['genre'].append()
            data['genre'] = [{'slug': genre} for genre in genres]
        ret = super().to_internal_value(data)
        return ret
'''