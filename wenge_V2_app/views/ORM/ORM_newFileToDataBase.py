
from wenge_V2_app import models


def newFileToDataBase(data):
    # models.account.objects.all().delete() # for test
    print('目前运行:  newFileToDataBase(data) :')
    # 数据结构如下 : 
    # 第一层:data = {'status':200,'tag':fileName,'data':data}
    # 第二层:data = {'sucess': {1: {'username': 'Soltero6192@lcoool.top', 'password': 'HW6ctP7Y9'}, 2: {'username': 'Soltero6192@lcoool.top', 'password': 'HW6ctP7Y9'}},'fail':{}}
    print(data)
    print('正准备写入数据',data['data']['sucess'])
    fail = 0
    fail_list = []
    for key, value in data['data']['sucess'].items():
        username = value['username']
        password = value['password']
        extraEmail = value['extraEmail']
        print('extraEmail:',extraEmail)
         # new lord in data ,default status = 0
        # models.account.objects.create(username=username,password=password,extraEmail = extraEmail,usedByPhone='None',status=0,tag=data['tag']) # for test
        try:
            models.account.objects.create(
                username=username,
                password=password,
                extraEmail = extraEmail,
                usedByPhone='None',
                status=0,
                tag=data['tag'])
        except:
            
            fail_list.append([username,password])
            fail = fail + 1
            print("写入失败 :",username,password)
    
    print('已完成ORM 数据库写入')
    print('导入失败 : ',fail_list)
    print('导入失败共计 : ',fail)

   

