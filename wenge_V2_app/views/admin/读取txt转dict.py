
# txt_path = "/Users/hudenis/Desktop/hide/Python/自制案例/Django_/wenge/胖d.txt"
# FileNameFullPath = txt_path

def txtToDict(FileNameFullPath) -> dict :
    with open(FileNameFullPath, 'r') as f:
        accountsData = f.read()
        accountsData = accountsData.split('\n')
        dict_0 = {'sucess':{},'fail':{}}
        id_sucess = 1
        id_fail = 1
        for each_line in accountsData:
            # print(each_line.text.split('----'))
            each_line = each_line.text
            try:
                str_3 = each_line.split('----')
                账号 = str_3[0]
                密码 = str_3[1]
                try:
                    extraEmail= str_3[2]
                except:
                    extraEmail = None
                print('id:', id_sucess, '账号:', 账号, '密码:', 密码,'extraEmail:',extraEmail)
                dict_0['sucess'][id_sucess] = {'account': 账号, 'password': 密码,'extraEmail:':extraEmail}
                id_sucess = id_sucess + 1
            except:
                # fail
                # 输出错误信息
                print()
                dict_0['fail'][id_fail] = {'line':each_line}
                print(id_fail, '解析失败')
                id_fail = id_fail + 1

    return dict_0

