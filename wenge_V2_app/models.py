from django.db import models
from django.utils import timezone


class account(models.Model):
    # 永久表
    # tiktok account permanent
    username = models.CharField(max_length=50) # 用户名
    password = models.CharField(max_length=50) # 密码
    status_choices = (
        # status 二选一 , 0 为未激活, 1 为已激活
        (0, "未使用"),
        (1, "已使用"),
    ) # 是否被使用
    status = models.IntegerField(choices=status_choices,default=0)
    tag = models.CharField(max_length=50) # 每一份上传docx文件,用文件名做tag
    extraEmail = models.CharField(max_length=50,default=None) # 辅助邮箱 ,可能有可能无
    usedByPhone = models.CharField(max_length=100,default=None) # 绑定手机,phoneName 不关联
    createdTime = models.DateTimeField(default=timezone.now) # 筛选最新列表用,Django 会在创建新对象时自动将该字段设置为当前时间




class phone(models.Model):
    # phone ID
    phoneId = models.AutoField(primary_key=True) # 主键
    phoneName = models.CharField(max_length=50) # 手机身份证
    lastLoginTime = models.DateTimeField(auto_now=True) # 最近一次登录时间
    cookie = models.CharField(max_length=300) # cookie ,没想好怎么写
    tiktokId = models.CharField(max_length=50,default=None) # 绑定了哪一个 tiktok 账号
    IP = models.CharField(max_length=200,default=None) # 绑定了哪一个 IP , 功能还没写好







