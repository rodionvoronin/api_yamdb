from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models import Avg
# from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminUserOrReadOnly, IsAdminModeratOrAuthorPermission, AdminOnly

from api.serializers import (
    CategorySerializer, GenreSerializer, TitleGetSerializer, SignUpSerializer, 
    TitleNotGetSerializer, ReviewSerializer, CommentSerializer, UsersSerializer, 
    NotAdminSerializer, GetTokenSerializer
)
from api.filters import TitleFilter
from reviews.models import Category, Genre, Title, Review, User


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Нет такого пользователя!'},
                status=status.HTTP_404_NOT_FOUND)
        if default_token_generator.check_token(user,
                                               data['confirmation_code']):
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        username_taken = User.objects.filter(username=username).exists()
        email_taken = User.objects.filter(email=email).exists()
        if email_taken and not username_taken:
            return Response('email занят', status=400)
        if username_taken and not email_taken:  # чужое имя
            return Response('username занят', status=400)
        user, flag = User.objects.get_or_create(
            username=username,
            email=email)
        code = default_token_generator.make_token(user)
        email_body = (
            f'Здраствуте, {user.username}.'
            f'\nКод подтверждения: {code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения '
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminUserOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleGetSerializer
        return TitleNotGetSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratOrAuthorPermission,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)
    

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly,)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminUserOrReadOnly,)

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratOrAuthorPermission,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
