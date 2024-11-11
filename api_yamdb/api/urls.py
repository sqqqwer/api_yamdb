from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet

router_api_v1 = DefaultRouter()
router_api_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                       ReviewViewSet,
                       basename='review'
                       )

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
