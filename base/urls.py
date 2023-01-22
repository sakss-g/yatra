from django.urls import path
from . import views

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

    #enduser related urls
    path('registerenduser/', views.register_enduser, name='register_enduser')
]
