from django.http import HttpResponse
from django.shortcuts import render
from wenge_V2_app import models

HomePage_Phone_remove_binding_path = "phone/HomePage_Phone_remove_binding.html" # delete cookie page path

def remove_binding(request):
    # 功能: 此手机解绑 , 账号是否回归账号池
    # 1. 获取phoneId    根据 cookie
    phoneId = request.COOKIES.get('phoneId')

    # 2. 获取tiktokId     获取此手机绑定的tiktokId
    tiktokId = models.phone.objects.get(phoneId=phoneId).tiktokId

    # 3. 解绑操作    , 找出本手机id,orm 换掉 tiktokId 为 'None
    models.phone.objects.filter(phoneId=phoneId).update(tiktokId='None')



    remove_account = request.GET.get('removeAccount')
    # 如果 removeAccount 参数存在并且值为 "yes"
    if remove_account == 'yes':
        models.account.objects.filter(id=tiktokId).update(status=2) # status=2 ,已封禁
        models.account.objects.filter(id=tiktokId).update(usedByPhone='None')
    elif remove_account == 'no':
        # 没封号,回归账号池
        models.account.objects.filter(id=tiktokId).update(status=0) # status=0 ,未使用
        models.account.objects.filter(id=tiktokId).update(usedByPhone='None')


   
    message = '解绑成功'
    response = HttpResponse(render(request, HomePage_Phone_remove_binding_path, {'message':message,}))
    
    return response