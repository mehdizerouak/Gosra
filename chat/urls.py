from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('', home, name="home"),

    path('chat-rooms/', chat_rooms, name='chat-rooms'),
    path('create-room/', create_room, name='create-room'),
    path('room/<str:room_name>/' , public_chat_room, name='public-chat-room'),

    path('users/', users_list, name='users-list'),
    path('message/<str:username>/', message_user, name='message-user'),
]
