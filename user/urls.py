from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('registration/', views.registration, name='registration'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('change_account', views.change_account, name='change_account')
]