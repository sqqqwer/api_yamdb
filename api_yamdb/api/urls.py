from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from api.views import CommentsViewSet, ReviewsViewSet, TitlesViewSet

router_v1 = DefaultRouter()
router_v1.register('titles/', TitlesViewSet, basename='titles')
router_v1.register(
    'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='reviews'
)
router_v1.register(
    'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/signup/', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]
