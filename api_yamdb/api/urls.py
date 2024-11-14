from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, RegistrationView, ReviewViewSet, TitleViewSet, TokenView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('titles/', TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet,
    basename='comment'
)
router_v1.register('users/', UserViewSet, basename='user')

auth_list = [
    path('signup/', RegistrationView, basename='signup'),
    path('token/', TokenView, basename='token'),
]

urlpatterns = [
    path('auth/', include(auth_list)),
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]
urlpatterns = [path('v1/', include(urlpatterns))]
