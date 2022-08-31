from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name="index"),
    path('', views.NLPView.as_view(), name="nlp"),
]
