from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import username_validator


class SignupSerializer(serializers.Serializer):
    """
    User registration serializer.
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        required=True, validators=[username_validator]
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Username {username} занят, выберите другой имя пользователя.'
            )
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f'{email} уже зарегистрирован, введите другой email.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """
    Token request serializer.
    """
    username = serializers.CharField(
        max_length=150, required=True, validators=[username_validator]
    )
    confirmation_code = serializers.CharField(max_length=255, required=True)


class UserSerializer(serializers.ModelSerializer):
    """
    User data serializer.
    """

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserPatchMeSerializer(UserSerializer):
    """
    User self data serializer.
    """
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class GetTitleSerializer(serializers.ModelSerializer):
    """
    Title serializer for GET requests
    """
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )


class TitleSerializer(serializers.ModelSerializer):
    """
    Title serializer for POST requests
    """
    genre = SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

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
