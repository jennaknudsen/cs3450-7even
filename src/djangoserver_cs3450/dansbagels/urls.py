from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prototype1/', views.prototype1, name='prototype1'),
    path('prototype1/changepassword', views.changepassword, name='changepassword'),
]
