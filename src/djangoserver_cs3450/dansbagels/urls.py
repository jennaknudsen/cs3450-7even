from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('prototype2/', views.prototype2, name='prototype2'),
    path('prototype1/', views.prototype1, name='prototype1'),
    path('prototype1/changepassword', views.changepassword, name='changepassword'),
    path('login/prototypelogin', views.prototype_login, name='prototype_login'),
    path('login/prototypelogout', views.prototype_logout, name='prototype_logout'),
    path('createAccount', views.createAccount, name='createAccount'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('orderBagel', views.orderBagel, name='orderBagel'),
    path('account', views.account, name='account'),
    path('admin/database', views.admin__database, name='admin__database'),
    path('deleteAccount', views.deleteAccount, name='deleteAccount'),
    path('placeOrder', views.placeOrder, name='placeOrder'),
    path('activeOrders', views.activeOrders, name='activeOrders'),
    path('completedOrders', views.completedOrders, name='completedOrders'),
    path('inventory', views.inventory, name='inventory'),
    path('cancelOrder', views.cancelOrder, name="cancelOrder"),
    path('createMenuItem', views.createMenuItem, name='createMenuItem'),
    path('reorder', views.reorder, name="reorder")
]
