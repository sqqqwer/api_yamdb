import random
import string

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import response, status, viewsets
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAuthorOrReadOnly, UserEmail, CorrectToken
from api.serializers import ReviewSerializer, EmailValidationSerializer, TokenSerializer, TokenReturn
from yamdb.models import Review
import jwt
from api_yamdb.settings import SIMPLE_JWT


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


class EmailValidationViewSet(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = EmailValidationSerializer
    permission_classes = (UserEmail,)

    def perform_create(self, serializer):
        confirmation_code = ''.join(random.choice(string.ascii_letters) for i in range(5))

        msg = EmailMultiAlternatives(
            "Subject here",
            confirmation_code,
            "from@example.com",
            [get_object_or_404(User, self.request.user).email],
        )
        msg.send()
        serializer.save(confirmation_code=confirmation_code)


class TokenViewSet(CreateAPIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        token = jwt.encode(
            payload={
                SIMPLE_JWT['USER_FIELD_ID']: get_object_or_404(User, username=request.data['username']).id
            },
            key=SIMPLE_JWT['SIGNING_KEY'],
            algorithm=SIMPLE_JWT['ALGORITHM']
        )
        serializer = TokenReturn(token=token)
        return Response(serializer.data, status=status.HTTP_200_OK)
