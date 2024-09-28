from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chatroom/<str:chatroom>/', PublicChatConsumer.as_asgi()),
    path('ws/private-chat/<str:username>/', PrivateChatConsumer.as_asgi()),
]