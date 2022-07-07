from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view()),

    path('create/', views.CreateUser.as_view()),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view),

    path('update/<pk>', views.UpdateView.as_view()),
    path('delete/<pk>', views.DeleteView.as_view()),

    path('list/', views.UserList.as_view(), name='clients'),
    path('like/', views.like_view),
]

# https://docs.google.com/document/d/1LpUf2cZdtDAZKgDP9zw7i8Qn98r7og0p8QqizZkMfhE/edit?usp=sharing