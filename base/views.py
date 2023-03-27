import datetime
from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.contrib import messages
from django.urls import reverse
from yatra.settings import KHALTI_API_KEY
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.core.mail import EmailMessage
from django.db.models import Count


import requests
import json
# Create your views here.
def handle_payment(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    u = request.build_absolute_uri(reverse('host_vehicles'))
    payload = json.dumps({
        "return_url": u,
        "website_url": u,
        "amount": 13000,
        "purchase_order_id": "test12",
        "purchase_order_name": "rajesh",
    })
    headers = {
        'Authorization': KHALTI_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.json()["payment_url"] is None:
        return redirect(response.json()["detail"])
    else:
        return redirect(response.json()["payment_url"])

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
                    if user.host.is_blocked == True:
                        logout(request)
                        messages.error(request, "You have been blocked")
                        return redirect('home')
                    return redirect('host_profile')
                elif str(user.groups.first()) == 'enduser':
                    if user.enduser.is_blocked == True:
                        logout(request)
                        messages.error(request, "You have been blocked")
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
    dates = list()
    for h in history:
        dates.append(h.start_date.strftime("%Y-%m-%d"))
        dates.append(h.end_date.strftime("%Y-%m-%d"))
        date_range = h.end_date - h.start_date
        for days in range(1, date_range.days):
            dates.append((h.start_date + datetime.timedelta(days)).strftime("%Y-%m-%d"))
    if request.method == "POST":
        start_date = request.POST.get('start')
        print(type(start_date))
        print(start_date)
        end_date = request.POST.get('end')
        print(end_date)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        print(current_date)
        can_rent = True
        if request.user.is_anonymous:
            messages.error(request, "You need to be a verified user to rent")
        elif start_date <= current_date:
            messages.error(request, "Start Date cannot be today or before now")
        elif end_date <= start_date:
            messages.error(request, "End Date cannot be before Start Date")
        elif vehicle.is_rented:
            for hist in history:
                sd = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                ed = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                date_range1 = hist.end_date - hist.start_date
                date_range2 = ed -sd

                if date_range1.days > date_range2.days:
                    for days in range(0, date_range1.days+1):
                        if ed == hist.start_date + datetime.timedelta(days) or sd == hist.start_date + datetime.timedelta(days):
                            messages.error(request, "Vehicle already booked for this date range!!!")
                            can_rent = False
                            break
                else:
                    for days in range(0, date_range2.days+1):
                        if hist.start_date == sd+datetime.timedelta(days) or hist.end_date == sd+datetime.timedelta(days):
                            messages.error(request, "Vehicle already booked for this date range!!!")
                            can_rent = False
                            break
                if not can_rent:
                    break

            if can_rent:
                try:
                    rent = Rents()
                    rent.renter = request.user.enduser
                    rent.vehicle = vehicle
                    rent.start_date = start_date
                    rent.end_date = end_date
                    rent.save()
                    vehicle.save()
                    messages.success(request, "Vehicle Rented")
                    return redirect('view_vehicles')
                except Exception as e:
                    print(e)
                    messages.error(request, "Error!!!! Could not rent")
        else:
            try:
                rent = Rents()
                rent.renter = request.user.enduser
                rent.vehicle = vehicle
                rent.start_date = start_date
                rent.end_date = end_date
                rent.save()
                vehicle.is_rented = True
                vehicle.save()
                messages.success(request,"Vehicle Rented")
                return redirect('view_vehicles')
            except Exception as e:
                print(e)
                messages.error(request, "Error!!!! Could not rent")
    context = {
        'vehicle': vehicle,
        'history':history,
        'dates':dates
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
            host = host_documents_form.save(commit=False)
            host.is_approved = "Pending"
            host.save()
            return redirect('host_profile')
    context = {
        'form': host_documents_form
    }
    return render(request, 'host/host_upload_documents.html', context)


def host_vehicles(request):
    error = ''
    if request.GET.get('pidx') is not None:
        transaction = Transaction()
        transaction.host = request.user.host
        transaction.amount = request.GET.get('amount')
        transaction.t_id = request.GET.get('transaction_id')
        transaction.save()
    elif request.GET.get('message') is not None:
        error = request.GET.get('message')

    vehicle_list = Vehicle.objects.filter(host=request.user.host)
    transactions = Transaction.objects.filter(host__user=request.user)
    if transactions.count() == 0:
        add_payment = 'yes'
    else :
        add_payment = 'no'

    context = {
         'vehicle_list' : vehicle_list,
         'add_payment': add_payment,
         'error':error
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


def rented_history(request):
    history = Rents.objects.filter(vehicle__host=request.user.host)
    context = {
        'history': history,
    }

    return render(request, 'host/rented_history.html', context)


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

def host_dashboard(request):
    return render(request, 'host/host_dashboard.html')


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
            enduser = enduser_documents_form.save(commit=False)
            enduser.is_approved = "Pending"
            enduser.save()
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
def view_transaction(request):
    transaction = Transaction.objects.all()
    paginator = Paginator(transaction, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'data': page_obj,
        'nums': page_obj.paginator.num_pages * 'p',
        'transactions':transaction,
    }

    return render(request, 'admin/all_transactions.html',  context)


def delete_user(request, pk):
    user = User.objects.filter(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def admin_dashboard(request):
    hosts = Host.objects.all()
    endusers = EndUser.objects.all()
    
    total_user_count = (hosts.filter(is_approved="Approved")).count()+(endusers.filter(is_approved="Approved")).count()
    pending_user_count = (hosts.filter(is_approved="Pending")).count()+(endusers.filter(is_approved="Pending")).count()
    rejected_user_count = (hosts.filter(is_approved="Rejected")).count()+(endusers.filter(is_approved="Rejected")).count()

    hosts_count = hosts.filter(is_approved="Approved").count()
    endusers_count = endusers.filter(is_approved="Approved").count()

    vehicles = Vehicle.objects.all()

    approved_vehicle_count = vehicles.filter(is_approved="Approved").count()
    pending_vehicle_count = vehicles.filter(is_approved="Pending").count()
    rejected_vehicle_count = vehicles.filter(is_approved="Rejected").count()

    vehicle_type_count = Vehicle.objects.all().count()
    if vehicle_type_count > 0:
        vehicle_types = Vehicle.objects.values('type').annotate(total=Count('type'))
        # print(vehicle_types)
    else:
        vehicle_types = None


    # fyp_count = StudentTopic.objects.all().count()
    # if fyp_count > 0:
    #     fyp_titles = StudentTopic.objects.values('field').annotate(total=Count('field'))
    #     print(fyp_titles)
    # else:
    #     fyp_titles = None



    travelogues = Travelogue.objects.all()
    
    approved_travelogue_count = travelogues.filter(is_approved="Approved").count()
    pending_travelogue_count = travelogues.filter(is_approved="Pending").count()
    rejected_travelogue_count = travelogues.filter(is_approved="Rejected").count()


    reports = ReportUser.objects.all()

    pending_report_count = reports.filter(status='Pending').count()
    noaction_report_count = reports.filter(status='NoAction').count()
    warning_report_count = reports.filter(status='Warning').count()
    blocked_report_count = reports.filter(status='Blocked').count()


    context={
        'total_user_count':total_user_count,
        'pending_user_count': pending_user_count,
        'rejected_user_count': rejected_user_count,

        'approved_vehicle_count': approved_vehicle_count,
        'pending_vehicle_count': pending_vehicle_count,
        'rejected_vehicle_count': rejected_vehicle_count, 

        'approved_travelogue_count': approved_travelogue_count,
        'pending_travelogue_count': pending_travelogue_count,
        'rejected_travelogue_count': rejected_travelogue_count,

        'pending_report_count': pending_report_count,
        'noaction_report_count': noaction_report_count,
        'warning_report_count': warning_report_count,
        'blocked_report_count': blocked_report_count,

        'hosts_count': hosts_count,
        'endusers_count': endusers_count,

        'vehicle_types': vehicle_types,
    }
    return render(request, 'admin/admin_dashboard.html', context)


def end_users_admin(request):
    nameform = UserFilterForm(request.GET or None)
    if nameform.is_valid():
        endUsers = nameform.filter_users(EndUser.objects.all())
    else:
        endUsers = EndUser.objects.filter(is_approved="Approved")

    statusform = UserFilterStatusForm(request.GET or None)

    if statusform.is_valid():
        endUsers = statusform.filter_users(endUsers)
    else:
        endUsers = endUsers.filter(is_approved="Approved")

    paginator = Paginator(endUsers, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'data': page_obj,
        'nums': page_obj.paginator.num_pages * 'p',
        'nameform': nameform,
        'statusform':statusform
    }
    return render(request, 'enduser/endusers_admin.html', context)


def hosts_admin(request):
    nameform = UserFilterForm(request.GET or None)
    if nameform.is_valid():
        hosts = nameform.filter_users(Host.objects.all())
    else:
        hosts = Host.objects.filter(is_approved="Approved")

    statusform = UserFilterStatusForm(request.GET or None)

    if statusform.is_valid():
        hosts = statusform.filter_users(hosts)
    else:
        hosts = hosts.filter(is_approved="Approved")

    paginator = Paginator(hosts, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'data': page_obj,
        'nums': page_obj.paginator.num_pages * 'p',
        'nameform': nameform,
        'statusform':statusform
    }
    # hosts = Host.objects.all()
    # context={
    #     'users':hosts
    # }
    return render(request, 'host/hosts_admin.html', context)


def verify_user(request):
    unverified_hosts = Host.objects.filter(is_approved="Pending")
    unverified_endusers = EndUser.objects.filter(is_approved="Pending")
    paginatorh = Paginator(unverified_hosts, 8)
    paginatore = Paginator(unverified_endusers, 8)
    page_number = request.GET.get('page')

    try:
        page_objh = paginatorh.get_page(page_number)
    except PageNotAnInteger:
        page_objh = paginatorh.get_page(1)
    except EmptyPage:
        page_objh = paginatorh.get_page(paginatorh.num_pages)

    try:
        page_obje = paginatore.get_page(page_number)
    except PageNotAnInteger:
        page_obje = paginatore.get_page(1)
    except EmptyPage:
        page_obje = paginatore.get_page(paginatore.num_pages)

    context = {
        'datah': page_objh,
        'numsh': page_objh.paginator.num_pages * 'p',
        'datae': page_obje,
        'numse': page_obje.paginator.num_pages * 'p',
    }
    return render(request,'admin/verify_user.html', context)

def open_citizenship(request, pk):
    citizenship = Host.objects.get(id=pk).citizenship.path
    return FileResponse(open(citizenship, 'rb'))    

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


def hosting_request(request):
    form = StatusFilterForm(request.GET or None)
    if form.is_valid():
        filter=request.GET.get('is_approved')
        unverified_vehicles = form.filter_report(Vehicle.objects.all())
    else:
        filter='Pending'
        unverified_vehicles = Vehicle.objects.filter(is_approved='Pending')
    
    context = {
        'unverified_vehicles': unverified_vehicles ,
        'filter': filter,
        'form': form
    }

    return render(request, 'admin/hosting_request.html',context)


def approve_travelogue(request, pk):
    if request.method == "POST":
        travelogue = Travelogue.objects.get(id=pk)
        travelogue.is_approved = "Approved"
        travelogue.save()
    return redirect('verify_travelogue')


def reject_travelogue(request, pk):
    if request.method == "POST":
        travelogue = Travelogue.objects.get(id=pk)
        travelogue.is_approved = "Rejected"
        travelogue.save()
    return redirect('verify_travelogue')


def verify_travelogues(request):
    form = StatusFilterForm(request.GET or None)
    if form.is_valid():
        filter=request.GET.get('is_approved')
        unverified_travelogue = form.filter_report(Travelogue.objects.all())
    else:
        filter='Pending'
        unverified_travelogue = Travelogue.objects.filter(is_approved='Pending')
    context = {
        'unverified_travelogue': unverified_travelogue,
        'filter': filter,
        'form': form
    }

    return render(request, 'admin/verify_travelogues.html',context)


def view_reports(request):
    form = ReportFilterForm(request.GET or None)
    if form.is_valid():
        filter=request.GET.get('status')
        reports = form.filter_report(ReportUser.objects.all())
    else:
        filter='Pending'
        reports = ReportUser.objects.filter(status='Pending')

    context = {
        'reports':reports,
        'filter': filter,
        'form':form
    }

    return render(request, 'admin/view_reports.html', context)

def handle_report(request, pk, fk):
    if request.method == "POST":
        report = ReportUser.objects.get(id=pk)
        print(report)
        if fk == 1:
            report.status = 'NoAction'
            report.save()
        elif fk == 2:
            if report.to.groups.filter(name='host').exists():
                host = report.to.host
                host.is_blocked = True
                host.save()
            else:
                enduser = report.to.enduser
                enduser.is_blocked = True
                enduser.save()
            report.status = 'Blocked'
            report.save()
        # print(request.user.groups.filter(name='enduser').exists())
        elif fk == 3:
            report.status = 'Warning'
            report.save()
            email = EmailMessage(
                'Warning Notification',
                'There has been complaints against you and you service. Continuing to get complaints will get you blocked',
                'sakss.hi19@gmail.com',
                [report.to.username],
            )
            email.send(fail_silently=False)
        elif fk == 4:
            if report.to.groups.filter(name='host').exists():
                host = report.to.host
                host.is_blocked = False
                host.save()
            else:
                enduser = report.to.enduser
                enduser.is_blocked = False
                enduser.save()
            report.status = 'NoAction'
            report.save()
        return redirect('view_reports')


# travelogues related views
def all_travelogues(request):
    travelogues = Travelogue.objects.filter(is_approved="Approved")
    allow = False
    if request.user.groups.filter(name='enduser').exists():
        enduser = request.user.enduser
        rents = Rents.objects.filter(renter = enduser)
        if rents.count() > 0:
            allow = True
    context = {
        'travelogues_list':travelogues,
        'allow':allow
    }
    return render(request, 'travelogues/travelogues.html', context)


def submit_travelogue(request):
    submit_travelogue_form = SubmitTravelogueForm()

    if request.method == "POST":
        submit_travelogue_form = SubmitTravelogueForm(request.POST, request.FILES)
        if submit_travelogue_form.is_valid():
            submit_travelogue = submit_travelogue_form.save(commit=False)
            submit_travelogue.enduser = request.user.enduser
            submit_travelogue.save()
            return redirect('travelogues_uploaded') 
        else:
            messages.error(request, submit_travelogue_form.errors)
    context = {
    'form': submit_travelogue_form
    }
    return render(request, 'travelogues/submit_travelogue.html', context)


def travelogues_uploaded(request):
    travelogues = Travelogue.objects.filter(enduser=request.user.enduser)
    context = {
        'uploaded_travelogues': travelogues 
    }
    return render(request, 'enduser/travelogues_uploaded.html', context)


def open_travelogue(request, pk):
    travelogue = Travelogue.objects.get(id=pk).image1.path
    return FileResponse(open(travelogue, 'rb'))


#userprofile
def view_profile_enduser(request, pk):
    enduser = EndUser.objects.get(id=pk)
    renthistory = Rents.objects.filter(renter=enduser, vehicle__host=request.user.host)
    report = ReportUser.objects.filter(by=request.user, to=enduser.user)
    if report.count() > 0:
        report_button = False
    else:
        report_button = True
    context = {
        'enduser': enduser,
        'renthistory': renthistory,
        'report_button': report_button
    }
    return render(request, 'host/enduser_profile.html', context)

def view_profile_host(request, pk, fk):
    host = Host.objects.get(id=pk)
    vehicles = Vehicle.objects.filter(host=host)
    rent = Rents.objects.get(id=fk)
    ratings = RateRent.objects.filter(rent__vehicle__host=host).aggregate(avg=Avg('rating'))
    try:
        rate = RateRent.objects.get(rent__id=fk)
        form = None
    except:
        rate = None
        form = RateRentForm()

    context={
        'host':host,
        'vehicles':vehicles,
        'rate':rate,
        'rent':rent.id,
        'form':form,
        'ratings':ratings['avg']
    }
    return render(request, 'enduser/host_profile.html', context)


# report and rating related views
def report_user(request, to):
    reportform = ReportUserForm()

    if request.method == "POST":
        reportform = ReportUserForm(request.POST, request.FILES)
        if reportform.is_valid():
            report = reportform.save(commit=False)
            report.by = request.user
            report.to = User.objects.get(id=to)
            report.save()
            if request.user.groups.filter(name='host').exists():
                return redirect('rented_history')
            elif request.user.groups.filter(name='enduser').exists():
                return redirect('renting_history')

    context = {
        'form':reportform
    }
    return render(request, 'reprat/report.html', context)

def rate_rent(request, pk):
    rent = Rents.objects.get(id=pk)
    form = RateRentForm(request.GET)
    if form.is_valid():
        rate = form.save(commit=False)
        rate.rent = rent
        rate.save()
    else:
        print("Invalid form")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



