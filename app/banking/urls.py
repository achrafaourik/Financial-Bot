from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('accounts', views.BankAccountViewSet)

app_name = 'banking'

urlpatterns = [
    path('', include(router.urls)),
]
