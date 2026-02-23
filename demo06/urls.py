"""
URL configuration for demo06 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from repair.views import repair,inquire,update,delete,get_userMaterial_data
from index.views import old_index
from register.views import register, calendar_shifts_api
from login.views import login,logout
from title_announcement.views import index
from title_announcement.views import editor
from title_announcement.views import announcement_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('repair/get', repair, name='repair'),
    path('repair/', repair, name='repair'),
    path('inquire/', inquire, name='inquire'),
    path('update/<str:pk>', update, name='update'),
    path('delete/<str:pk>', delete, name='delete'),
    path('old_index/', old_index, name='old_index'),
    path('register/', register, name='register'),
    path('login/',login, name='login'),
    path('logout/',logout,name='logout'),
    path('index/', index, name='index'),
    path('editor.html', editor, name='editor'),

    path('announcement/<int:announcement_id>/', announcement_detail, name='announcement_detail'),
    
    # API 
    path('register/api/calendar-shifts/', calendar_shifts_api, name='calendar_shifts_api'),
    path('repair/get_userMaterial_data', get_userMaterial_data, name='get_userMaterial_data'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

