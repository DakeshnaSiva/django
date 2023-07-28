from django.shortcuts import render,redirect
from django.http import HttpResponse
from.models import Room,Topic, Message
from.forms import Room_form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# rooms=[
#     {'id':1,'name':"Lets learn python"},
#     {'id':2,'name':"Design"},
#     {'id':3,'name':"Frontend devlopment"},
# ]
def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exit')

    context={'page':page}
    return render(request,'dk/login_register.html',context)
    
def logoutuser(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    form=UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request,'dk/login_register.html',{'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
)
    room_count=rooms.count()
    topics=Topic.objects.all
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_message':room_message}
    return render(request,'dk/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        room.save()
        return redirect('room', pk=room.id)

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'dk/room.html',context)

def userprofile(request,pk):
    user=User.objects.get(id=pk) 
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,
             'room_messages': room_messages,'topics':topics}
    return render(request,'dk/profile.html',context)

@login_required(login_url='login')
def createroom(request):
    form = Room_form()
    if request.user  == form.instance.host:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        form = Room_form(request.POST)
        if form.is_valid():  # added this line
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'dk/room_form.html', context)

@login_required(login_url='login')
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    form=Room_form(instance=room)
    if request.user != form.instance.host:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        form = Room_form(request.POST,instance=room)
        if form.is_valid():  # added this lineD
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'dk/room_form.html', context)

@login_required(login_url='login')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'dk/delete.html', context)

@login_required(login_url='login')
def delete_message(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    context={'obj':message}
    return render(request,"dk/delete message.html",context)
