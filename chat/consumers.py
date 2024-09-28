import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class PublicChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['chatroom']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        room = self.room_group_name
        await self.save_message_db(username, message, room)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def save_message_db(self, username, message, room):
        room = ChatRoom.objects.get(name=self.room_group_name)
        user = User.objects.get(username=username)
        message = ChatRoomMessage(sender=user, content=message, room=room)
        message.save()


# ===============================================================================

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username1 = self.scope['user'].username
        username2 = self.scope['url_route']['kwargs']['username']
        # sorting usernames in the room name string alphabetically cuz we need the same room name in both sides
        room_name = f'{min(username1,username2)}_{max(username1,username2)}'
        self.room_group_name = f'chat_{room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        receiver_username = text_data_json['receiver_username']

        await self.save_message_db(username, receiver_username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'private_message',
                'message': message,
                'username': username,
            }
        )

    async def private_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def save_message_db(self, sender, receiver, message):

        sender = User.objects.get(username=sender)
        receiver = User.objects.get(username=receiver)
        
        room = PrivateRoom.get_or_create_private_room(sender, receiver)
        message = PrivateRoomMessage(room=room, sender=sender, content=message)
        message.save()