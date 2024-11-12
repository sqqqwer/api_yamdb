from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import jwt
from rest_framework import response, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken

from api import serializers
from api.permissions import IsAuthorOrReadOnly
from api.serializers import ReviewSerializer
from api.utils import Util
from yamdb.models import Review, User


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


class SignUp(GenericAPIView):
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        # getting tokens
        user_email = User.objects.get(email=user['email'])
        tokens = RefreshToken.for_user(user_email).access_token
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://'+current_site+relative_link+"?token="+str(tokens)
        email_body = 'Hi '+user['username'] + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user['email'],
                'email_subject': 'Verify your email'}

        Util.send_email(data=data)

        return response.Response({'user_data': user, 'access_token': str(tokens)}, status=status.HTTP_201_CREATED)


class VerifyEmail(GenericAPIView):
    serializer_class = serializers.EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return response.Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return response.Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return response.Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
