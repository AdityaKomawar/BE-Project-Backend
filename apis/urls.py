from django.urls import path

from .views import ListSingleImage ,DetailSingleImage

urlpatterns = [
  path('<int:pk>/', DetailSingleImage.as_view()),
  path('', ListSingleImage.as_view()),
  # path('<int:pk>/', DetailSingleImage),
  # path('', ListSingleImage),
]
