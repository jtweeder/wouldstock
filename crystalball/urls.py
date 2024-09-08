from django.urls import path
from . import views as crystalball_views

urlpatterns = [
    path('', crystalball_views.index, name='index'),
    path('ticker/<str:ticker>/', crystalball_views.ticker, name='ticker'),
]