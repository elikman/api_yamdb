from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from api.utils import generate_confirmation_code, send_confirmation_email
from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import CONST_EMAIL_LENGTH, CONST_USERNAME_LENGTH
from users.models import CinemaUser as User
from users.roles import Roles
from users.validators import validate_username_me


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Метод для валидации данных."""

        request = self.context['request']
        if request.method == 'POST':
            user = request.user
            title_id = request.parser_context['kwargs']['title_id']
            if Review.objects.filter(title_id=title_id, author=user).exists():
                raise ValidationError(
                    'Вы уже оставляли отзыв на это произведение'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения информации о произведении."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового произведения."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=False,
        allow_empty=False
    )

    class Meta:
        """Метод, преобразующий данные в представление."""

        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя"""
    username = serializers.CharField(
        max_length=CONST_USERNAME_LENGTH,
        validators=[
            UnicodeUsernameValidator(),
            validate_username_me
        ],
        error_messages={
            'blank': 'This field may not be blank.',
            'required': 'This field is required.',
            'unique': 'A user with that username already exists.',
        }
    )
    email = serializers.EmailField(
        max_length=CONST_EMAIL_LENGTH,
        error_messages={
            'blank': 'This field may not be blank.',
            'required': 'This field is required.',
            'unique': 'A user with that email already exists.',
            'invalid': 'Enter a valid email address.',
        }
    )

    def validate(self, data):
        """Метод для валидации данных"""
        try:
            User.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'A user with that username or email already exists.'
            )
        return data

    def create(self, validated_data):
        """Метод для создания нового пользователя"""
        username = validated_data['username']
        email = validated_data['email']

        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            defaults={'is_active': False, 'role': Roles.USER.value}
        )
        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()

        send_confirmation_email(user.email, confirmation_code)
        return user


class CreateTokenSerializer(serializers.Serializer):
    """Сериализатор для создания токена доступа."""

    username = serializers.CharField(max_length=CONST_USERNAME_LENGTH)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                "Недействительный код подтверждения.")

        data['user'] = user
        return data

    def create(self, validated_data):
        """Метод для валидации данных."""

        user = validated_data['user']
        user.save()
        token = AccessToken.for_user(user)
        return {'access': token}
