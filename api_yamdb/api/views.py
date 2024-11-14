import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

import jwt
from api.permissions import IsAuthorOrReadOnly
from api.serializers import RegistrationSerializer, ReviewSerializer, TokenReturnSerializer, TokenSerializer
from api_yamdb.settings import SIMPLE_JWT
from yamdb.models import Review


User = get_user_model()


# временный класс для тестов
class CommentViewSet(viewsets.ModelViewSet):
    pass


# временный класс для тестов
class TitleViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class RegistrationView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        confirmation_code = ''.join(random.choice(string.ascii_letters) for i in range(5))
        msg = EmailMultiAlternatives(
            "Code of api_yamdb",
            confirmation_code,
            "from@example.com",  # тут не знаю, от кого
            [get_object_or_404(User, self.request.user).email],
        )
        msg.send()
        serializer.save(confirmation_code=confirmation_code)


# есть подозрение, что нам надо сделать так https://habr.com/ru/articles/793058/
class TokenView(CreateAPIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        token = jwt.encode(
            payload={
                SIMPLE_JWT['USER_FIELD_ID']: get_object_or_404(User, username=request.data['username']).id
            },
            key=SIMPLE_JWT['SIGNING_KEY'],
            algorithm=SIMPLE_JWT['ALGORITHM']
        )
        serializer = TokenReturnSerializer(token=token)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = User
