from django.http import HttpResponse
from django.shortcuts import render
from wenge_V2_app import models

phone_change_id_path = "phone/phone_change_id.html" # html page path

def phone_change_id(request):
    change_id_to = request.GET.get('change_id')
    message = '此手机已改为 : '+change_id_to
    
    response = HttpResponse(render(request, phone_change_id_path, {'message':message,}))
    response.set_cookie('phoneId', change_id_to, max_age=60*60*24*365*2)