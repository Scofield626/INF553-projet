from django.urls import path

from . import views

app_name = 'inf553'
urlpatterns = [
    path('', views.index, name='index'),
    path('<table>/', views.detail, name = 'detail'),
]
