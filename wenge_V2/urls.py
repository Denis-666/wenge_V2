"""wenge_V2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import wenge_V2_app.views.phone.HomePage_Phone as HomePage_Phone
import wenge_V2_app.views.phone.HomePage_Phone_remove_binding as HomePage_Phone_remove_binding
import wenge_V2_app.views.admin.HomePage_admin as HomePage_admin
import wenge_V2_app.views.ORM.ORM_testing as ORM_testing
import wenge_V2_app.views.Cookie.Cookie_test as Cookie_test
import wenge_V2_app.views.login.login as login
import wenge_V2_app.views.phone.phone_change_id as phone_change_id



urlpatterns = [
    # phone
    path('', HomePage_Phone.HomePage_Phone),
    path('remove_binding/', HomePage_Phone_remove_binding.remove_binding),
    path('change_id/', phone_change_id.phone_change_id),

    path('admin/', HomePage_admin.HomePage_Admin),
    path('admin/test', HomePage_admin.test),
    path('orm/test',ORM_testing.ORM_testing),
    path('cookie/test',Cookie_test.set_cookie),

    # login testing
    path('login/',login.login),

    
]
