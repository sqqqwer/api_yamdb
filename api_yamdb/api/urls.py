from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet,
    RegistrationView,
    ReviewViewSet,
    TitleViewSet,
    TokenView,
    CategoryViewSet,
    GenreViewSet,
    UserMeView,
    UserViewSet
)


router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register('users', UserViewSet, basename='user')

auth_pattern = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('token/', TokenView.as_view(), name='token'),
]

urlpatterns_v1 = [
    path('users/me/', UserMeView.as_view(), name='userme'),
    path('auth/', include(auth_pattern)),
    path('', include(router_v1.urls)),
]

urlpatterns = [path('v1/', include(urlpatterns_v1))]
