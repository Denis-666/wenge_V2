from django.shortcuts import render
from django.http import HttpResponse

HomePage_Phone_path = "phone/HomePage_Phone.html" # html page path

def set_cookie(request):
    response = render(request, HomePage_Phone_path)
    response.set_cookie('my_cookie', 'cookie_value123', max_age=3600)
    return response