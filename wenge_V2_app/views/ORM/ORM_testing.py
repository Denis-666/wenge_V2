
from django.http import HttpResponse
from django.utils import timezone
from wenge_V2_app.models import account
from datetime import timedelta
from datetime import datetime
from wenge_V2_app import models

# 假设 data.createdTime 是一个 datetime 对象



def ORM_testing(request):
    tag = '20谷歌'
    # 2. 根据这个 tag 获取 status=0 ,的第一条数据 ,返回id
    # orm 返回数据
    ormResponse = models.account.objects.filter(status=9,tag=tag).first()
    print('ormResponse:',ormResponse)
    if ormResponse == None:
        print('没号了,已经用完')
    else:
        # 3. 再根据id获取:邮箱,密码,tag
        tiktokId = ormResponse.id
        email = ormResponse.username
        password = ormResponse.password
        tag =ormResponse.tag

    return HttpResponse("ORM_testing:"+tag+'_'+email+'_'+password)



def ORM_按最新时间搜索(request):

    data = account.objects.all().order_by('-createdTime').first()
    print('data:',data.username,data.password,data.extraEmail,data.status,data.tag,data.createdTime)
    print('data createdTime:',data.createdTime)
    minute_str = data.createdTime.strftime('%Y-%m-%d %H:%M')
    print('minute_str:',minute_str)

    # 假设 minute_str 是从 data.createdTime 转换而来的字符串
    start_time = datetime.strptime(minute_str, '%Y-%m-%d %H:%M')
    end_time = start_time.replace(second=59, microsecond=0) + timedelta(minutes=1)

    # 假设你的模型名为 MyModel
    results = account.objects.filter(createdTime__gte=start_time, createdTime__lt=end_time).all()
    print('results:',results)
    for i in results:
        print(i.username,i.password,i.extraEmail,i.status,i.tag,i.createdTime)
    return HttpResponse("ORM_testing",data)