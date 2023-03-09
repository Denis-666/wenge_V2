import os
from wenge_V2_app.views.admin.读取docx转dict import docxToDict
from wenge_V2_app.views.admin.读取txt转dict import txtToDict

def uploadFileToDict(fileFullPath) -> dict :
    print('目前运行:  uploadFileToDict(fileFullPath) -> dict :')
    # getAccountDataFromUploadFilToDict
    status = {'status':200,'data':None}
    filePath = fileFullPath # 写 fileFullPath 是提醒自己,这里是完整的地址(不管相对还是绝对)
    # 判断文件是否存在
    data_dict = {} # init
    if os.path.exists(filePath):
        print('文件存在 路径是:',filePath)
        fileSuffix = os.path.splitext(filePath)[1]# 获取文件后缀名 后 : 两种方法 docx , txt
        if fileSuffix == '.docx':
            data_dict = docxToDict(filePath)  # docxToJson 这是包含后缀名的
            status = {'status':200,'data':data_dict} 
            return status
        elif fileSuffix == '.txt':
            data_dict = txtToDict(filePath)  # txtToJson 这是包含后缀名的
            status = {'status':200,'data':data_dict} 
            return status
        print('目前只能识别 txt,docx两种格式')
        status = {'status':404,'data':data_dict} 
        return status
    else:
        print('文件不存在 路径是:',filePath)
        status = {'status':404,'data':None}    
        return status


