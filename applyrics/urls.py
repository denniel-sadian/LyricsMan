from django.urls import path
from . import views

app_name = 'applyrics'
urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('<str:letter>/', views.letter_list, name='letter'),
    path('<str:letter>/<int:pk>/', views.lyrics, name='lyrics'),
]
