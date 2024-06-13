from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('register',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('create_post',views.create_post,name='create_post'),
    path('post/<str:pk>',views.post,name='post'),
    path('like_post/<str:pk>',views.like_post,name='like'),
    path('profile_picture_change/<str:pk>',views.profile_picture_change,name='profile_picture_change'),
    path('edit_post/<str:pk>',views.edit_post,name='edit'),
    path('delete_post/<str:pk>',views.delete_post,name='delete'),
    path('create_post',views.create_post,name='create'),
    path('search',views.search,name='search'),
    path('follow/<str:pk>',views.follow,name='follow'),

    

    

]