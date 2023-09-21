from django.contrib import admin
from django.urls import path, include
from user_system import views

from user_system.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('', Home.as_view(), name='home'),
    path('download/', views.download_data, name='download_data'),
    path('delete/', views.delete_data, name='delete_data'),
    path('accounts/profile/', Home.as_view(), name='profile'),
]
