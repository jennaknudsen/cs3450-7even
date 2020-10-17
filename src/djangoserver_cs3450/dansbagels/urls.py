from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('prototype2', views.prototype2, name='prototype2'),
    path('prototype1/', views.prototype1, name='prototype1'),
    path('prototype1/changepassword', views.changepassword, name='changepassword'),
]
