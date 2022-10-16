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


class GetTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)

    def validate(self, data):
        if datetime.date.today().year < data['year']:
            raise serializers.ValidationError(
                'Publication year can not be later then current year!'
            )
        return data

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = genre
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
                current_genre = genre
                lst.append(current_genre)
            instance.genre.set(lst)

        instance.save()
        return instance
