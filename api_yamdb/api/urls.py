from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet, TitleViewSet, EmailValidationViewSet, TokenViewSet

router_v1 = DefaultRouter()
router_v1.register('titles/', TitleViewSet, basename='title')
router_v1.register(
    'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register('auth/signup/', EmailValidationViewSet, basename='signup')
router_v1.register('auth/token/', TokenViewSet, basename='token')

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]
urlpatterns = [path('v1/', include(urlpatterns))]
