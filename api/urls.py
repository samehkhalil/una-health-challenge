from django.urls import path
from . import views

urlpatterns = [
    path('levels/', views.LevelList.as_view(), name="level-list"),
    path('levels/<str:pk>', views.LevelDetail.as_view(), name="level-detail"),
    path('prepopulate/', views.LevelDataPrePopulate.as_view(), name="prepopulate"),
]