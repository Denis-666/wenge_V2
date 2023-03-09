from django.shortcuts import render
from django.http import HttpResponse
from models import models
# response
from django.http import HttpResponseRedirect

HomePage_Phone_path = "phone/HomePage_Phone.html" # html page path

def Cookie_phone(request):
    # 没写好，不要用
    
    cookie = request.COOKIES.get('phone_cookie')
    # cookie processing 
    # 1. 如果没有cookie，就赋予新cookie
    # 2. 如果有cookie，就读取cookie
    if cookie == None:
        # set cookie
        pass
    else:
        # read cookie
        pass

    message = ''
    data = ''
    response = render(request, HomePage_Phone_path,{'message':message,'upload_data':data})
    response.set_cookie('my_cookie', 'cookie_value123', max_age=3600)
    return response