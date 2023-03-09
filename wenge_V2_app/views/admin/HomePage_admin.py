from django.shortcuts import render
from wenge_V2_app.models import account
import json
import os
from django.http import HttpResponse
from wenge_V2_app import models
from wenge_V2_app.views.admin.uploadFileToDict import uploadFileToDict
from wenge_V2_app.views.ORM.ORM_newFileToDataBase import newFileToDataBase
from docx import Document 

fileSavePath = "./uploadFile/" # 保存上传文件用
HomePage_admin_Path = 'admin/HomePage_admin.html'



def HomePage_Admin(request):
    # Admin 页面 v2
    # 功能:
    # 1. 上传文件,读取文件,写入数据库 (POST)
    # 2. 读取目前数据库Tiktok号,并返回前端渲染 (GET)

    if request.method == 'POST':
        # 1. 接受文件
        latest_accounts_data = 0 # inti
        message,fileName = uploadFile(request)
        fileType = fileName.split('.')[-1]
        tag = fileName.split('.')[0] # 获取 tag 作为分类
        result = models.account.objects.filter(tag=tag)
        if result.count() != 0 :  
            # 检测是否已经上传?   ,这个tag是否已经使用过?           
            message = '这个文件已经上传过,请改新的文件名,本次操作并不会修改数据库'
        else:
            # 数据库没有同样tag,允许上传      
        # 2. 读取文件,写入数据库
            fileFullPath = os.path.join(fileSavePath,fileName)
            len_sucess = 0 # init 成功数量
            len_fail = 0 # init 失败数量
            if fileType == 'docx':
                document = Document(fileFullPath)
                for paragraph in document.paragraphs:
                    try:
                        str_3 = paragraph.text.split('----')
                        username = str_3[0]
                        password = str_3[1]
                        try:
                            extraEmail = str_3[2]
                        except:
                            extraEmail = 'None'
                        models.account.objects.create(
                            username=username,
                            password=password,
                            extraEmail = extraEmail,
                            usedByPhone='None',
                            status=0,
                            tag=tag)
                        len_sucess += 1
                        print('成功写入单次:',username,password,extraEmail,tag)
                    except:
                        print('失败写入单次:',paragraph.text)
                        len_fail += 1
                        continue
                print('成功写入共计:',len_sucess)
                print('失败写入共计:',len_fail)
                latest_accounts_data = account.objects.filter(tag=tag).all()
                message = '上传成功 : '+ str(tag)
            else:
                message = '文件格式错误,请上传docx格式文件'

        # 3. 前端渲染
        return render(request, HomePage_admin_Path, {'latest_accounts_data': latest_accounts_data,'message':message})



    if request.method == 'GET':
        # 1. 直接查找最近一次上传的tag,并根据这个tag查找数据库,返回前端渲染
        
        data = account.objects.all().order_by('-createdTime').first() # 获取最新的一条数据,里面的 tag ,tag是标签,是文件名
        if latest_accounts_data != None:
            tag = data.tag
            message = '最新上传表格为:'+str(tag)+',内容如下:'
        else:
            tag = 'None'

        latest_accounts_data = account.objects.filter(tag=tag).all()
        if latest_accounts_data == None:
            message = '数据库为空,请上传文件'


    
        return render(request, HomePage_admin_Path, {'latest_accounts_data': latest_accounts_data,'message':message})



## testing model

def test(request):
    # inject_old_data() # 注入旧数据 test model
    change_status_to_0()
    print('hello this is testing')
    return render(request, "admin/HomePage_admin.html")


# 把 account 里面 status 全部改为0
def change_status_to_0():
    accounts = account.objects.all()
    for each_account in accounts:
        each_account.status = 0
        each_account.save()

# 注入旧数据
def inject_old_data():
    json_path = 'json_0.json'
    with open(json_path, 'r') as f:
        data = json.load(f)

    for each_data in data:
        print(each_data)
        account.objects.create(username=each_data['account'], password=each_data['password'])


# for file upload
def uploadFile(request):
    print('目前运行:  uploadFile(request) :')
    message = 'no files for upload!'
    if request.method == 'POST':
        # 获取上传的文件，如果没有文件，则默认为None
        myFile = request.FILES.get("avatar", None)
        if not myFile:
            message = '并没有成功接收文件,上传失败'
            fileName = None
        else:
            # 打开特定的文件进行二进制的写操作
            destination = open(os.path.join(fileSavePath, myFile.name), 'wb+')
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            message =  '文件上传成功 : '
            print('message: ',message)
            fileName = myFile.name
    return message,fileName



def HomePage_Admin_v1(request):
    # 封存
    pass
    # if request.method == 'POST':
    # # 1. 这里 POST 负责处理文件上传后写入数据库

    #     message,fileName = uploadFile(request)

    #     fileFullPath = os.path.join(fileSavePath,fileName)
    #     data = {'status':0,'tag':0,'data':{'sucess_len':0,'fail_len':0,'sucess':{},'fail':{}}} # init data structure
    #     data = uploadFileToDict(fileFullPath) # File To Dict
    #     if data['status'] == 200:
    #         data['tag'] = fileName.split('.')[0]
    #         print('新上传数据正常,开始写入数据库ORM',data['tag'])

    #         # 计算 成功 和 失败 统计
    #         num_success = 0
    #         for key in data['data']['sucess']:
    #             num_success += 1
    #         data['data']['sucess_len'] = num_success
    #         print('num_success',num_success)
    #         print("data['data']['sucess_len'] : ",data['data']['sucess_len'])
    #         num_fail = 0
    #         for key in data['data']['fail']:
    #             num_fail += 1
    #         data['data']['fail_len'] = num_fail

            
            
    #         result = models.account.objects.filter(tag=data['tag'])
    #         if result.count() != 0 :  
    #             # 检测是否已经上传?   ,这个tag是否已经使用过?           
    #             message = '这个文件已经上传过,请改新的文件名,本次操作并不会修改数据库'
    #             data = {'status':403,'tag':0,'data':{'sucess_len':0,'fail_len':0,'sucess':{},'fail':{}}} # 错误 403 ,自创,表示文件已经上传过
    #             latest_accounts_data = 0
    #             print(message)                
    #         else:
    #             message = '上传成功!!'
    #             print(message)
    #             newFileToDataBase(data) # data 数据结构 : data = {'status':0,'tag':0,'data':{'sucess_len':0,'fail_len':0,'sucess':{},'fail':{}}}
    #             db_data = account.objects.all().order_by('-createdTime').first() # 获取最新的一条数据,里面的 tag ,tag是标签,是文件名
    #             tag = db_data.tag
    #             message = '最新上传表格为:'+str(tag)+',内容如下:'
    #             latest_accounts_data = account.objects.filter(tag=tag).all() 

    #     if data['status'] == 404 or data['data']['sucess_len'] == 0 :
    #         print('新上传数据错误,拒绝写入数据库ORM')
    #         message = '上传数据错误,应该是格式问题,详细联系管理员'
    #         data = {'status':404,'tag':0,'data':{'sucess_len':0,'fail_len':0,'sucess':{},'fail':{}}} # init data structure
    #         latest_accounts_data = 0

    #     return render(request, HomePage_admin_Path, {'latest_accounts_data': latest_accounts_data,'message':message})
