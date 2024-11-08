from django.urls import path
from .views import *
urlpatterns = [
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('register/',registerUser,name='register'),
    path('',home,name='home'),
    path('add/',add,name='add'),
    path('update/<int:pk>',updateTask,name='update'),
    path('delete/<int:pk>',deleteTask,name='delete'),
    path('details/',details,name='details'),
]