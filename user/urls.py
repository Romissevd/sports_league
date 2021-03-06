from django.urls import path, re_path
from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('change_account/', views.change_account, name='change_account'),
    path('users', views.all_users, name='users'),
    re_path(r'account/(?P<name>[A-z@._/]+)/', views.account),
]