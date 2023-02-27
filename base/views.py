import datetime
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User, Group
from .models import Host, EndUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.contrib import messages
# Create your views here.

# all related views
def home(request):
    return render(request, 'base/home.html')


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
                    return redirect('host_profile')
                elif str(user.groups.first()) == 'enduser':
                    return redirect('home')
                else:
                    message = "User group was not found"
                    return render(request, 'base/login.html', {'error':message})
        else:
            message = "User was not found"
            return render(request, 'base/login.html', {'error':message})
    return render(request, 'base/login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


def view_vehicles(request):
    vehicles = Vehicle.objects.filter(is_approved="Approved")
    context = {
        'vehicle_list':vehicles,
    }
    return render(request, 'vehicles/view_vehicles.html', context)

def vehicle_details(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    history = Rents.objects.filter(vehicle=vehicle)
    if request.method == "POST":
        start_time = request.POST.get('start')
        end_time = request.POST.get('end')
        current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        can_rent = True
        if request.user.is_anonymous:
            messages.error(request, "You need to be a verified user to rent")
        elif start_time <= current_time:
            messages.error(request, "Start Time cannot be before now")
        elif end_time <= start_time:
            messages.error(request, "End Time cannot be before Start Time")
        elif vehicle.is_rented:

            for hist in history:
                if (hist.start_time.strftime("%Y-%m-%dT%H:%M") <= start_time <= hist.end_time.strftime("%Y-%m-%dT%H:%M")) \
                        or (hist.start_time.strftime("%Y-%m-%dT%H:%M") <= end_time <= hist.end_time.strftime("%Y-%m-%dT%H:%M")):
                    messages.error(request, "Vehicle has already been booked for this period")
                    can_rent = False
                    break
            if can_rent:
                try:
                    rent = Rents()
                    rent.renter = request.user.enduser
                    rent.vehicle = vehicle
                    rent.start_time = start_time
                    rent.end_time = end_time
                    rent.save()
                    vehicle.is_rented = True
                    vehicle.save()
                    messages.success(request, "Vehicle Rented")
                    return redirect('view_vehicles')
                except:
                    messages.error(request, "Error!!!! Could not rent")
        else:
            try:
                rent = Rents()
                rent.renter = request.user.enduser
                rent.vehicle = vehicle
                rent.start_time = start_time
                rent.end_time = end_time
                rent.save()
                vehicle.is_rented = True
                vehicle.save()
                messages.success(request,"Vehicle Rented")
                return redirect('view_vehicles')
            except:
                messages.error(request, "Error!!!! Could not rent")
    context = {
        'vehicle': vehicle,
        'history':history,
    }
    return render(request, 'vehicles/vehicle_detail.html', context)

# host related views
def register_host(request):
    host_form = HostForm()

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
        host_form = HostForm(request.POST, instance=host)

        if host_form.is_valid:
            host_form.save()
            return redirect('login') 

    return render(request, 'host/register_host.html', {'form':host_form})


@login_required
def host_dashboard(request):
    return render(request, 'host/host_dashboard.html')


def host_profile(request):
    return render(request, 'host/host_profile.html')


def host_update_profile(request):
    host = request.user.host
    host_update_form = HostUpdateForm(instance=host)

    if request.method == "POST":
        host_update_form = HostUpdateForm(request.POST, request.FILES, instance=host)
        if host_update_form.is_valid():
            host_update_form.save()
            return redirect('host_profile')
    context = {
        'host_update_form': host_update_form
    }
    return render(request, 'host/host_update_profile.html', context)


def host_upload_documents(request):
    host = request.user.host
    host_documents_form = HostDocumentsForm(instance=host)

    if request.method == "POST":
        host_documents_form = HostDocumentsForm(request.POST, request.FILES, instance=host)
        if host_documents_form.is_valid():
            host_documents_form.save()
            return redirect('host_profile')
    context = {
        'form': host_documents_form
    }
    return render(request, 'host/host_upload_documents.html', context)


def host_vehicles(request):
    vehicle_list = Vehicle.objects.filter(host=request.user.host)

    context = {
         'vehicle_list' : vehicle_list
    }
    return render(request, 'vehicles/host_vehicles.html', context)


def add_vehicles(request):
    vehicle_form = VehicleForm()

    if request.method == "POST":
        vehicle_form = VehicleForm(request.POST, request.FILES)
        if vehicle_form.is_valid():
            vehicle = vehicle_form.save(commit=False)
            vehicle.host = request.user.host
            vehicle.save()
            return redirect('host_vehicles') 
        else:
            messages.error(request, vehicle_form.errors)
    context = {
    'form': vehicle_form
    }
    return render(request, 'vehicles/add_vehicles.html', context)

def update_vehicles(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    vehicle_update_form = VehicleForm(instance=vehicle)

    if request.method == "POST":
        vehicle_update_form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if vehicle_update_form.is_valid():
            vehicle_update_form.save()
            messages.success(request, 'Vehicle Updated.')
            return redirect('host_vehicles')

    context = {
        'form': vehicle_update_form,
        'vehicle_form': vehicle
    }
    return render(request, 'vehicles/update_vehicles.html', context)

def delete_vehicles(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    vehicle.delete()
    return redirect('host_vehicles')


def approve_vehicle(request, pk):
    if request.method == "POST":
        vehicle = Vehicle.objects.get(id=pk)
        vehicle.is_approved = "Approved"
        vehicle.save()
    return redirect('hosting_request')

def reject_vehicle(request, pk):
    if request.method == "POST":
        vehicle = Vehicle.objects.get(id=pk)
        vehicle.is_approved = "Rejected"
        vehicle.save()
    return redirect('hosting_request')

def open_bluebook(request, pk):
    bluebook = Vehicle.objects.get(id=pk).bluebook.path
    return FileResponse(open(bluebook, 'rb'))

def open_vehicle(request, pk, no):
    vehicle = Vehicle.objects.get(id=pk)
    if no == 1:
        vehicle = vehicle.image1.path
    elif no == 2:
        vehicle = vehicle.image2.path
    elif no == 3:
        vehicle = vehicle.image3.path
    return FileResponse(open(vehicle, 'rb'))

def open_vehicle2(request):
    image2 = Vehicle.objects.get().image2.url
    return FileResponse(open(image2, 'rb'))

def open_vehicle3(request):
    image3 = Vehicle.objects.get().image3.path
    return FileResponse(open(image3, 'rb'))



# end users related views
def register_enduser(request):
    enduser_form = EndUserForm()

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
        enduser_form = EndUserForm(request.POST, instance=host)

        if enduser_form.is_valid:
            enduser_form.save()
            return redirect('login') 

    return render(request, 'enduser/register_enduser.html', {'form':enduser_form})


def enduser_dashboard(request):
    return render(request, 'enduser/enduser_dashboard.html')


def enduser_profile(request):
    return render(request, 'enduser/enduser_profile.html')


def enduser_update_profile(request):
    enduser = request.user.enduser
    enduser_update_form = EndUserUpdateForm(instance=enduser)

    if request.method == "POST":
        enduser_update_form = EndUserUpdateForm(request.POST, request.FILES, instance=enduser)
        if enduser_update_form.is_valid():
            enduser_update_form.save()
            return redirect('enduser_profile')
    context = {
        'enduser_update_form': enduser_update_form
    }
    return render(request, 'enduser/enduser_update_profile.html', context)


def enduser_upload_documents(request):
    enduser = request.user.enduser
    enduser_documents_form = EndUserDocumentsForm(instance=enduser)

    if request.method == "POST":
        enduser_documents_form = EndUserDocumentsForm(request.POST, request.FILES, instance=enduser)
        if enduser_documents_form.is_valid():
            enduser_documents_form.save()
            return redirect('enduser_profile')
    context = {
        'form': enduser_documents_form
    }
    return render(request, 'enduser/enduser_upload_documents.html', context)

def renting_history(request):
    history = Rents.objects.filter(renter=request.user.enduser)

    context = {
        'history':history,
    }

    return render(request, 'enduser/renting_history.html', context)

# admin related views

def delete_user(request, pk):
    user = User.objects.filter(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def admin_dashboard(request):
    host_count = Host.objects.all().count()
    enduser_count = EndUser.objects.all().count()
    #vehicle_count = Vehicle.objects.all().count()
    #blog_count = Travelogue.objects.all().count()
    context={
        'hostcount':host_count,
        'endusercount':enduser_count,
        #'vehiclecount':vehicle_count,
        #'blogcount':blog_count
    }
    return render(request, 'admin/admin_dashboard.html', context)


def end_users_admin(request):
    endUsers = EndUser.objects.all()
    context={
        'users':endUsers
    }
    return render(request, 'enduser/endusers_admin.html', context)


def hosts_admin(request):
    hosts = Host.objects.all()
    context={
        'users':hosts
    }
    return render(request, 'host/hosts_admin.html', context)


def verify_user(request):
    unverified_hosts = Host.objects.filter(is_approved="Pending")
    unverified_endusers = EndUser.objects.filter(is_approved="Pending")
    context = {
        'unverified_endusers':unverified_endusers,
        'unverified_hosts':unverified_hosts
    }
    return render(request,'admin/verify_user.html', context)


def approve_host(request, pk):
    if request.method == "POST":
        host = Host.objects.get(id=pk)
        host.is_approved = "Approved"
        host.save()
        return redirect('verify_user')


def reject_host(request,pk):
    if request.method == "POST":
        host = Host.objects.get(id=pk)
        host.is_approved = "Rejected"
        host.save()
        return redirect('verify_user')


def approve_enduser(request, pk):
    if request.method == "POST":
        enduser = EndUser.objects.get(id=pk)
        enduser.is_approved = "Approved"
        enduser.save()
        return redirect('verify_user')


def reject_enduser(request,pk):
    if request.method == "POST":
        enduser = EndUser.objects.get(id=pk)
        enduser.is_approved = "Rejected"
        enduser.save()
        return redirect('verify_user')

# def verify_user(request):
#     unverified_hosts = Host.objects.filter(is_approved="Pending")
#     unverified_endusers = EndUser.objects.filter(is_approved="Pending")
#     context = {
#         'unverified_endusers':unverified_endusers,
#         'unverified_hosts':unverified_hosts
#     }
#     return render(request,'admin/verify_user.html', context)

def hosting_request(request):
    unverified_vehicles = Vehicle.objects.filter(is_approved="Pending")

    context = {
        'unverified_vehicles': unverified_vehicles
    }

    return render(request, 'admin/hosting_request.html',context)





