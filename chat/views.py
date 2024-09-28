from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'chat/home.html')

@login_required
def users_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/users.html', {'users':users})

@login_required
def chat_rooms(request):
    context = { 'rooms':ChatRoom.objects.all().order_by('-date_added') }
    return render(request, 'chat/chatrooms.html', context)

class Login(LoginView):
    template_name = 'chat/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')

class Register(CreateView):
    template_name = 'chat/register.html'
    model = User
    form_class = UserCreationForm

    def form_valid(self, form):
        self.object = form.save()
        return redirect('home')
    
@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST['title']
        description = request.POST['description']   
        room = ChatRoom(name=name, description=description)
        room.save()
        return redirect('home')
    else:
        return render(request, 'chat/create_room.html')
    

@login_required
def public_chat_room(request, room_name):
    room = ChatRoom.objects.get(name=room_name)
    messages = ChatRoomMessage.objects.filter(room=room).order_by('-date_added')[:10][::-1]
    context = {'room':room, 'messages':messages}

    return render(request, 'chat/public_chat_room.html', context)

@login_required
def message_user(request, username):
    sender = request.user
    recepient = User.objects.get(username=username)
    room = PrivateRoom.get_or_create_private_room(sender, recepient)
    messages = PrivateRoomMessage.objects.filter(room=room)

    context = {'messages':messages, 'recepient_username':username}

    return render(request, 'chat/private_chat_room.html', context)