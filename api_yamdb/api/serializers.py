from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from api.utils import generate_confirmation_code, send_confirmation_email
from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
from users.models import CinemaUser as User
from users.roles import RoleEnum
from users.validators import validate_username_me


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
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
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
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
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
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
        max_length=MAX_LENGTH_EMAIL,
        error_messages={
            'blank': 'This field may not be blank.',
            'required': 'This field is required.',
            'unique': 'A user with that email already exists.',
            'invalid': 'Enter a valid email address.',
        }
    )

    def validate(self, data):
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
        username = validated_data['username']
        email = validated_data['email']

        # Check if the user already exists
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            defaults={'is_active': False, 'role': RoleEnum.USER.value}
        )
        confirmation_code = generate_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()

        send_confirmation_email(user.email, confirmation_code)
        return user


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=MAX_LENGTH_USERNAME)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        # Validate the username exists
        user = get_object_or_404(User, username=username)

        # Validate the confirmation code
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError("Invalid confirmation code.")

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        user.is_active = True
        user.save()
        access = AccessToken.for_user(user)
        return {
            'access': str(access),
        }
