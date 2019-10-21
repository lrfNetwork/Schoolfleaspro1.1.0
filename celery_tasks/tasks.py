# 使用celery
import time
import os
import random
from random import shuffle

import django
from celery import Celery

# 导入发送邮件的类
from django.core.mail import send_mail
from django.conf import settings

# 创建一个Celery类的实例对象
from django.http import request

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/2')

# 初始化django 因为下面需要使用django本身的配置项settings.EMAIL_FROM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolFleasPro.settings')
django.setup()


# 定义任务函数
@app.task
def send_register_active_email(to_email, checkcodes):
    # 发送邮件
    subject = '【校园跳蚤】账户激活提醒'
    # 这个不能发html格式的邮件
    message = ''
    sender = settings.EMAIL_FROM  # 发件人
    reciver = [to_email]
    html_message = "<h1>尊敬的%s用户您好，欢迎注册校园跳蚤应用</h1>您的验证码为：%s" % (reciver, checkcodes)
    send_mail(subject, message, sender, reciver, html_message=html_message, fail_silently=False)
    # time.sleep()
    print(checkcodes)