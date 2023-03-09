from django.shortcuts import render
from docx import Document 

def ORM(request):
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
