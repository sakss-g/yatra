from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),

    #admin related urls
    path('admindashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('end_users_admin/', views.end_users_admin, name='end_users_admin'),        
    path('hosts_admin/', views.hosts_admin, name='hosts_admin'),        

    #host related urls
    path('registerhost/', views.register_host, name='register_host'),
    path('hostdashboard/', views.host_dashboard, name='host_dashboard'),
    path('hostprofile/', views.host_profile, name='host_profile'),
    path('host_update_profile/', views.host_update_profile, name='host_update_profile'),

    #enduser related urls
    path('registerenduser/', views.register_enduser, name='register_enduser'),
    path('enduserdashboard/', views.enduser_dashboard, name='enduser_dashboard'),
    path('enduserprofile/', views.enduser_profile, name='enduser_profile'),
    path('enduser_update_profile/', views.enduser_update_profile, name='enduser_update_profile'),
         
    #delete user
    path('deleteuser/<int:pk>', views.delete_user, name='delete_user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
