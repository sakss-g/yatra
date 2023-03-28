from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('handlepayment', views.handle_payment, name="handle_payment"),
    path('login/',views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),


    # admin related urls
    path('admindashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('end_users_admin/', views.end_users_admin, name='end_users_admin'),        
    path('hosts_admin/', views.hosts_admin, name='hosts_admin'),
    path('verify_user/', views.verify_user, name='verify_user'),
    path('approve_host/<str:pk>', views.approve_host, name='approve_host'),
    path('reject_host/<str:pk>', views.reject_host, name='reject_host'),
    path('approve_enduser/<str:pk>', views.approve_enduser, name='approve_enduser'),
    path('reject_enduser/<str:pk>', views.reject_enduser, name='reject_enduser'),
    path('hosting_request', views.hosting_request, name='hosting_request'),
    path('view_reports', views.view_reports, name='view_reports'),
    path('handle_report/<str:pk>/<int:fk>', views.handle_report, name='handle_report'),
    path('view_transactions/', views.view_transaction, name='view_transactions'),
    path('view_policies/', views.view_policies, name='view_policies'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('faqs/', views.faqs, name='faqs'),
    path('add_faqs/', views.add_faqs, name='add_faqs'),
    path('delete_faq/<str:pk>', views.delete_faq, name='delete_faq'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('add_terms_and_conditions/', views.add_terms_and_conditions, name='add_terms_and_conditions'),
    path('delete_terms_and_conditions/<str:pk>', views.delete_terms_and_conditions, name='delete_terms_and_conditions'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('add_privacy_policy/', views.add_privacy_policy, name='add_privacy_policy'),
    path('delete_privacy_policy/<str:pk>', views.delete_privacy_policy, name='delete_privacy_policy'),


    # host related urls
    path('registerhost/', views.register_host, name='register_host'),
    path('hostdashboard/', views.host_dashboard, name='host_dashboard'),
    path('hostprofile/', views.host_profile, name='host_profile'),
    path('host_update_profile/', views.host_update_profile, name='host_update_profile'),
    path('host_upload_documents/', views.host_upload_documents, name='host_upload_documents'),
    path('rented_history', views.rented_history, name='rented_history'),
    path('viewprofileenduser/<str:pk>', views.view_profile_enduser, name='view_profile_enduser'),
    path('host_dashboard/', views.host_dashboard, name='host_dashboard'),


    # enduser related urls
    path('registerenduser/', views.register_enduser, name='register_enduser'),
    path('enduserdashboard/', views.enduser_dashboard, name='enduser_dashboard'),
    path('enduserprofile/', views.enduser_profile, name='enduser_profile'),
    path('enduser_update_profile/', views.enduser_update_profile, name='enduser_update_profile'),
    path('enduser_upload_documents/', views.enduser_upload_documents, name='enduser_upload_documents'),
    path('renting_history/',views.renting_history, name="renting_history"),
    path('travelogues_uploaded/', views.travelogues_uploaded, name='travelogues_uploaded'),
    path('open_travelogue/<int:pk>', views.open_travelogue, name='open_travelogue'),
    path('viewprofilehost/<int:pk>/<int:fk>',views.view_profile_host, name='view_profile_host'),

    # delete user
    path('deleteuser/<int:pk>', views.delete_user, name='delete_user'),
    path('reportuser/<str:to>', views.report_user, name='report_user'),
    path('raterent/<int:pk>', views.rate_rent, name='rate_rent'),


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
    path('host_vehicles', views.host_vehicles, name='host_vehicles'),
    path('add_vehicles', views.add_vehicles, name='add_vehicles'),
    path('update_vehicles/<str:pk>', views.update_vehicles, name='update_vehicles'),
    path('delete_vehicles/<str:pk>', views.delete_vehicles, name='delete_vehicles'),
    path('approve_vehicle/<str:pk>', views.approve_vehicle, name="approve_vehicle"),
    path('reject_vehicle/<str:pk>', views.reject_vehicle, name="reject_vehicle"),

    # multi user urls
    path('openbluebook/<str:pk>', views.open_bluebook, name='open_bluebook'),
    path('openvehicle1/<str:pk>/<int:no>', views.open_vehicle, name='open_vehicle'),
    path('viewvehicles/',views.view_vehicles, name="view_vehicles"),
    path('vehiclesdetails/<str:pk>',views.vehicle_details, name="vehicle_details"),
    path('open_citizenship/', views.open_citizenship, name='open_citizenship'),


    # travelogues related urls
    path('all_travelogues/', views.all_travelogues, name='all_travelogues'),
    path('submit_travelogue/', views.submit_travelogue, name='submit_travelogue'),
    path('verify_travelogue/', views.verify_travelogues, name='verify_travelogue'),
    path('approve_travelogue/<str:pk>', views.approve_travelogue, name="approve_travelogue"),
    path('reject_travelogue/<str:pk>', views.reject_travelogue, name="reject_travelogue"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
