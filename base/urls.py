from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),


    #admin related urls
    path('admindashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('end_users_admin/', views.end_users_admin, name='end_users_admin'),        
    path('hosts_admin/', views.hosts_admin, name='hosts_admin'),
    path('verify_user/', views.verify_user, name='verify_user'),
    path('approve_host/<str:pk>', views.approve_host, name='approve_host'),
    path('reject_host/<str:pk>', views.reject_host, name='reject_host'),
    path('approve_enduser/<str:pk>', views.approve_enduser, name='approve_enduser'),
    path('reject_enduser/<str:pk>', views.reject_enduser, name='reject_enduser'),
    path('hosting_request', views.hosting_request, name='hosting_request'),


    #host related urls
    path('registerhost/', views.register_host, name='register_host'),
    path('hostdashboard/', views.host_dashboard, name='host_dashboard'),
    path('hostprofile/', views.host_profile, name='host_profile'),
    path('host_update_profile/', views.host_update_profile, name='host_update_profile'),
    path('host_upload_documents/', views.host_upload_documents, name='host_upload_documents'),


    #enduser related urls
    path('registerenduser/', views.register_enduser, name='register_enduser'),
    path('enduserdashboard/', views.enduser_dashboard, name='enduser_dashboard'),
    path('enduserprofile/', views.enduser_profile, name='enduser_profile'),
    path('enduser_update_profile/', views.enduser_update_profile, name='enduser_update_profile'),
    path('enduser_upload_documents/', views.enduser_upload_documents, name='enduser_upload_documents'),
    path('renting_history/',views.renting_history, name="renting_history"),

    #delete user
    path('deleteuser/<int:pk>', views.delete_user, name='delete_user'),


     # Forgot password and reset
    path('password_reset', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name="password_reset"),
    path('password_change', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html'), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name="password_change_done"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    
    # vehicles related urls
    path('hostvehicles', views.host_vehicles, name='host_vehicles'),
    path('addvehicles', views.add_vehicles, name='add_vehicles'),
    path('updatevehicles/<str:pk>', views.update_vehicles, name='update_vehicles'),
    path('deletevehicles/<str:pk>', views.delete_vehicles, name='delete_vehicles'),
    path('approvevehicle/<str:pk>', views.approve_vehicle, name="approve_vehicle"),
    path('rejectvehicle/<str:pk>', views.reject_vehicle, name="reject_vehicle"),

    # multi user urls
    path('openbluebook/<str:pk>', views.open_bluebook, name='open_bluebook'),
    path('openvehicle1/<str:pk>/<int:no>', views.open_vehicle, name='open_vehicle'),
    path('viewvehicles/',views.view_vehicles, name="view_vehicles"),
    path('vehiclesdetails/<str:pk>',views.vehicle_details, name="vehicle_details"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
