from django.shortcuts import render, redirect
from .forms import Form
from django.contrib.auth.models import User, Group
from .models import Host, EndUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def register_host(request):
    host_form = Form()

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create(username=email, password=make_password(password))
        group = Group.objects.get(name="host")
        print(group.name)
        user.groups.add(group)
        user.save()
        host = Host()
        host.user = user
        host_form = Form(request.POST, instance=host)

        if host_form.is_valid:
            host_form.save()
            return redirect('login') 

    return render(request, 'host/register_host.html', {'form':host_form})

def register_enduser(request):
    enduser_form = Form()

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create(username=email, password=make_password(password))
        group = Group.objects.get(name="enduser")
        print(group.name)
        user.groups.add(group)
        user.save()
        host = EndUser()
        host.user = user
        enduser_form = Form(request.POST, instance=host)

        if enduser_form.is_valid:
            enduser_form.save()
            return redirect('login') 

    return render(request, 'enduser/register_enduser.html', {'form':enduser_form})


def login_user(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            print("user was created and logged in")
            
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                if str(user.groups.first()) == 'host':
                    return redirect('host_dashboard')
                elif str(user.groups.first()) == 'enduser':
                    return redirect('home')
                else:
                    error = "User group was not found"
                    return render(request, 'base/login.html', {'error':error})
        else:
            error = "User was not found"
            return render(request, 'base/login.html', {'error':error})

    return render(request, 'base/login.html')

@login_required
def host_dashboard(request):
    return render(request, 'host/host_dashboard.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')

def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def end_users_admin(request):
    return render(request, 'enduser/end_users_admin.html')

def hosts_admin(request):
    return render(request, 'host/hosts_admin.html')