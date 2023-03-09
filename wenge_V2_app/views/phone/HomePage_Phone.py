from django.shortcuts import render

from django.template import loader

from wenge_V2_app.views.admin.uploadFileToDict import uploadFileToDict
from wenge_V2_app.views.ORM.ORM_newFileToDataBase import newFileToDataBase

from wenge_V2_app import models

from django.shortcuts import redirect# redirect 重定向


from datetime import datetime # datetime
from django.http import HttpResponse



HomePage_Phone_path = "phone/HomePage_Phone.html" # html page path


def ORM_newPhone_register(request):
    print('没有cookie,为新手机设置新cookie')
    # 若没cookie 就生成一个cookie,同时在服务器保存session
    # 要求: 1. 数据库找最多的id 再加1  2. 记录每一次的登录时间 3.为数据库增加一个手机用户
    
    # 1. 获取最新的电话号码并自增
    last_phone = models.phone.objects.last()
    phoneId = last_phone.phoneId + 1
    print('1. phoneId',phoneId)
    # 2. 记录访问时间    
    lastLoginTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('2. lastLoginTime',lastLoginTime)

    # 3 给与空值 tiktok account
    tiktokId = 'None'

    # 4. 为数据库增加一个手机用户,绑定 tiktokId
    phoneName = '手机'+ str(phoneId)
    models.phone.objects.create(
        phoneId=phoneId,
        phoneName=phoneName,
        lastLoginTime=lastLoginTime,
        cookie='no cookie',
        tiktokId = tiktokId,
        IP = 'None',
        )
    print('3. 为数据库增加一个手机用户')

    # 5. session
    request.session['phoneId'] = phoneId
    request.session['lastLoginTime'] = lastLoginTime

    # 6 . print 出结果
    print('这台手机使用账号 : id:',phoneId)

    return phoneId,lastLoginTime



def HomePage_Phone(request):
    uploadFile_status = 'no files for upload!' # init 
    # return HomePage_Phone_path
    template = loader.get_template(HomePage_Phone_path)
    # return html page



    if request.method == 'GET':
        # 功能: 展示出 本台手机 获取的tiktok账号密码
        message = '手机获取画面' # init 
        response = HttpResponse()
        # 1. cookie 处理 
        phoneId,lastLoginTime=cookie_processing(request) 

        # 2. 获取 phone_data
        phone_data = models.phone.objects.filter(phoneId=phoneId).first()

        # 3. 根据手机phone_data.tiktokId 获取 tiktok_accounts_data
        if phone_data.tiktokId == 'None':
            # 3.1 tiktokId == 'None' ,并没有绑定 tiktok账号 ,马上绑定
            tiktok_accounts_data = tiktok_accounts_data_processing(phone_data.phoneName)
            print('新cookie,本次账号 :',tiktok_accounts_data.username)
            print('新cookie,本次密码 :',tiktok_accounts_data.password)
        else:
            # 3.2 tiktokId != 'None' ,已经绑定 tiktok账号 ,直接获取
            tiktok_accounts_data = models.account.objects.filter(id=phone_data.tiktokId).first()
            print('旧cookie,本次账号 :',tiktok_accounts_data.username)
            print('旧cookie,本次密码 :',tiktok_accounts_data.password)
        # 4. 返回响应
        if tiktok_accounts_data == None:
            tiktok_accounts_data = {'username':'没有账号了','password':'没有账号了'}
            message = '没有账号了'
            response = HttpResponse(render(request, HomePage_Phone_path, {'message':message,'phone_data':phone_data,'tiktok_accounts_data':tiktok_accounts_data}))
            return response
        else:
            message = '获取账号成功'

        response = HttpResponse(render(request, HomePage_Phone_path, {'message':message,'phone_data':phone_data,'tiktok_accounts_data':tiktok_accounts_data}))
        response.set_cookie('lastLoginTime', lastLoginTime, max_age=365 * 24 * 60 * 60)
        response.set_cookie('phoneId', phoneId, max_age=365 * 24 * 60 * 60)
        return response



def cookie_processing(request):
    # 功能: 有就读取phoneId,没有就注册新手机
    cookie = request.COOKIES.get('phoneId')
    # 1. 处理cookie     , 把cookie拿去数据库查询,如果有,就返回数据,如果没有,就返回空

    if cookie == None:
        # 1.1 没cookie 
        # 1.1.1 注册一台新手机 
        phoneId,lastLoginTime = ORM_newPhone_register(request) # 去数据库 注册一台新手机  ,  已经获取了 email 和 password 
    else:
        # 1.2 有cookie 
        print('有cookie')
        # 1.2.1 获取 phoneId
        phoneId = request.COOKIES.get('phoneId')
        lastLoginTime = request.COOKIES.get('lastLoginTime')
        print('phoneId',phoneId)
        # 1.2.2 更新 lastLoginTime
        print('lastLoginTime',lastLoginTime)
        lastLoginTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        models.phone.objects.filter(phoneId=phoneId).update(lastLoginTime=lastLoginTime)

    return phoneId,lastLoginTime


def tiktok_accounts_data_processing(phoneName):
    # 功能 根据最新的tag,找到未使用的账号,提取出来

    # 1.找到最新的tag
    DB_data = models.account.objects.all().order_by('-createdTime').first() # 获取最新的一条数据,里面的 tag ,tag是标签,是文件名
    tag = DB_data.tag

    # 2. 根据这个 tag 获取 status=0 ,的第一条数据 ,返回id
    ormResponse = models.account.objects.filter(status=0,tag=tag).first()
    print('ormResponse:',ormResponse)
    if ormResponse == None:
        print('没号了,已经用完')
    else:
        tiktokId = ormResponse.id
        # 2.1 account 这个 tiktokId 改为 :已使用
        models.account.objects.filter(id=tiktokId).update(status=1)
        # 2.2 account 这个 tiktokId 绑定使用手机: phoneName
        models.account.objects.filter(id=tiktokId).update(usedByPhone=phoneName)
        # 2.3 phone 这个 phoneName 绑定 tiktokId
        models.phone.objects.filter(phoneName=phoneName).update(tiktokId=tiktokId)
    return ormResponse


