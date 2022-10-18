import datetime

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


def validate_username(username):
    """Проверка, что username не равно me"""

    if username in ('ME', 'me', 'Me', 'mE'):
        raise serializers.ValidationError(
            'Недопустимые имена: ME, me, Me, mE.'
        )
    return username


class SignupSerializer(serializers.Serializer):
    """Сериализатор для запроса кода подтверждения"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        required=True, validators=[validate_username]
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Username {username} занят, выберите другой имя пользователя.'
            )
        if (
            User.objects.filter(email=email).exists()
        ):
            raise serializers.ValidationError(
                f'{email} уже зарегистрирован, введите другой email.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериалайзер для запроса токена."""
    username = serializers.CharField(
        max_length=150, required=True, validators=[validate_username]
    )
    confirmation_code = serializers.CharField(max_length=255, required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserPatchMeSerializer(UserSerializer):
    """Сериализатор для работы со своим профилем."""
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )

    def get_rating(self, obj):
        title_reviews = Review.objects.filter(title_id=obj.pk)
        avg_rating = title_reviews.aggregate(Avg('score'))['score__avg']
        return avg_rating


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

    def validate_year(self, value):
        if datetime.date.today().year < value:
            raise serializers.ValidationError(
                'Год публикации не может быть позднее текущего года.'
            )
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = genre
            GenreTitle.objects.create(
                genre=current_genre, title=title
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценкой может быть целое число в диапазоне от 1 до 10.'
            )
        return value

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        second_review = (
            Review.objects.filter(author=author, title=title).exists()
        )
        if second_review:
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
