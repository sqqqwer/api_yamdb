from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CommentViewSet,
    RegistrationView,
    ReviewViewSet,
    TitleViewSet,
    TokenView,
    UserUsernameView,
    UserMeView,
    UserViewSet
)

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

user_list = [
    path('me/', UserMeView.as_view(), basename='me'),
    path('<slug:username>', UserUsernameView.as_view(), basename='username')
]


auth_list = [
    path('signup/', RegistrationView.as_view(), basename='signup'),
    path('token/', TokenView.as_view(), basename='token'),
]

urlpatterns = [
    path('users/', include(user_list)),
    path('auth/', include(auth_list)),
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]
urlpatterns = [path('v1/', include(urlpatterns))]
