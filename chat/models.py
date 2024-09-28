from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=70, unique=True)
    description = models.CharField(max_length=350)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} room"

class ChatRoomMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} message in {self.room.name}"
    
class PrivateRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1messages")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2messages")

    @classmethod
    def get_or_create_private_room(cls, user1, user2):
        # user 1 must have the smallest id
        users = [ user1 , user2 ]
        users.sort(key=lambda x: x.id)
        room , created = PrivateRoom.objects.get_or_create(user1=users[0], user2=users[1])

        return room
    
    def __str__(self):
        return f"{self.user1.username} & {self.user2.username} conversation"
    
class PrivateRoomMessage(models.Model):
    room = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Message from {self.sender.username} in {self.room}"