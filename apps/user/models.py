from django.db import models
# 导入django自带的user抽象类
# from django.contrib.auth.models import AbstractUser
# 导入定义的基类
from db.base_model import BaseModel


# Create your models here.

class User(BaseModel):
    """用户模型类"""
    STATUS_CHOICE = (
        (False, '正常'),
        (True, '黑名单'),
    )
    # user_id=models.IntegerField(verbose_name='用户id')
    username = models.CharField(max_length=20, verbose_name='用户名称')
    email = models.CharField(max_length=20, verbose_name='邮件')
    password = models.CharField(max_length=500, verbose_name='用户密码')
    last_login = models.DateTimeField(auto_now=True, verbose_name='最后登陆时间')
    headimg = models.ImageField(upload_to='user', verbose_name='头像')
    phone = models.CharField(max_length=20, verbose_name='电话')
    address = models.CharField(max_length=200, verbose_name='收货地址')
    user_token = models.CharField(max_length=500, verbose_name='用户token', default='')
    Blacklist = models.BooleanField(default=False, choices=STATUS_CHOICE, verbose_name='黑名单')

    class Meta:
        db_table = 'SchoolFleasPro_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.phone
