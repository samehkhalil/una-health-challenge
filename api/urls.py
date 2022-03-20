from django.urls import path
from . import views

urlpatterns = [
    path('levels/', views.LevelList.as_view()),
    path('levels/<str:pk>', views.LevelDetail.as_view()),
]