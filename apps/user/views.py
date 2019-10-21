from datetime import datetime
from random import shuffle
# 导入View抽象类post,get方法
from django.core.serializers import serialize
from django.views.generic import View

from django.http import JsonResponse

# 导入数据库模型
from django_redis import get_redis_connection

from apps.goods.models import Goods
from apps.user.models import User  # 这李绝对路径会报错，我也不知道为啥，百度的

# 异步发邮件
from celery_tasks.tasks import send_register_active_email

# 导入setting中的密文SECRET_KEY
from django.conf import settings

from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Json解析库
import json

# 阿里云核心SDK
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# 正则
import re

# hash加密
import hashlib


# Create your views here.
class RegisterView(View):
    def get(self, request):
        pass

    def post(self, request):
        r = json.loads(request.body)
        account = r['account']
        password = r['password']
        code = r['code']
        if judge_type(account) is None:
            return JsonResponse({'success': bool(False), 'msg': "账号格式有误！"})
        # 从redis缓存中读取缓存信息 account唯一
        check_code = cache.get(account)
        print(check_code)
        # 验证验证码是否正确
        if check_code == code:
            # 新加用户
            user = User()
            user.username = 'Sfleas_' + shuffle_str(True)[0:6]
            # 判断账号类型
            if judge_type(account) == 'phone':
                user.phone = account
            else:
                user.email = account
            # 密码加密
            user.password = encrypt(password)
            print(user.password)
            # 保存
            user.save()
            return JsonResponse({'success': bool(True), 'msg': "注册成功！"})
        else:
            return JsonResponse({'success': bool(False), 'msg': "验证码错误！"})


class SendVerifyView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 获取传过来的account
        r = json.loads(request.body)
        account = r['account']
        type = judge_type(account)
        if type is None:
            return JsonResponse({'success': bool(False), 'msg': "账号格式有误！"})
        elif type == 'email':
            email = account
            # 判断该邮箱是否已经被注册
            try:
                if User.objects.get(email=email):
                    return JsonResponse({'success': bool(False), 'msg': "该邮箱已被注册！"})
            except User.DoesNotExist:
                pass

            # 生成验证码
            check_code = shuffle_str()[0:6]  # 截取0-6位
            # 异步发送邮件
            send_register_active_email.delay(email, check_code)

            # 缓存到redis 设置5分钟过期
            cache.set(email, check_code, 300)
            return JsonResponse({'success': bool(True), 'msg': '发送成功！'})
        else:
            phone = account
            # 判断手机该是否已经被注册
            try:
                if User.objects.get(phone=phone):
                    return JsonResponse({'success': bool(False), 'msg': "该手机号已被注册！"})
            except User.DoesNotExist:
                pass

            # 生成验证码
            check_code = shuffle_str()[0:6]  # 截取0-6位

            # 发送短信
            resp = send_sms(phone, check_code)
            if resp == 'OK':
                # 缓存到redis 设置5分钟过期
                cache.set(phone, check_code, 300)
                return JsonResponse({'success': bool(True), 'msg': '发送成功！'})
            else:
                return JsonResponse({'success': bool(False), 'msg': resp})


class LoginView(View):
    def get(self, request):
        pass

    def post(self, request):
        r = json.loads(request.body)
        account = r['account']
        password = r['password']
        # 获取数据
        try:
            if judge_type(account) == 'email':
                user = User.objects.get(email=account)
            else:
                user = User.objects.get(phone=account)
            # 验证密码
            print(encrypt(password))
            if encrypt(password) == user.password:
                # 重写token
                token = encrypt(user.id, str(datetime.now()))
                # 保存token
                user.user_token = token
                user.save()
                return JsonResponse({'uid': user.id, 'success': bool(True), 'token': token})
            else:
                return JsonResponse({'success': bool(False), 'msg': '账号或密码错误'})
        except User.DoesNotExist:
            return JsonResponse({'success': bool(False), 'msg': '账户不存在'})


class AuthView(View):
    def get(self, request):
        pass

    def post(self, request):
        r = json.loads(request.body)
        uid = r['uid']
        token = r['token']
        try:
            user = User.objects.get(id=uid)
            if user.user_token == token:
                return JsonResponse({'success': bool(True)})
            else:
                return JsonResponse({'success': bool(False)})
        except User.DoesNotExist:
            return JsonResponse({'success': bool(False)})


def shuffle_str(alphabet=None):
    # 验证码字库
    if alphabet:
        check_str = 'abcdefg0123456789'
    else:
        check_str = '0123456789'
    # 将字符串转换成列表
    str_list = list(check_str)
    # 调用random模块的shuffle函数打乱列表
    shuffle(str_list)
    # 将列表转字符串
    return ''.join(str_list)


# 加密
def encrypt(content, confusion=None):
    # 创建一个hash对象
    h = hashlib.sha256()
    # 提升密码复杂度，防止直接解密
    h.update(settings.SECRET_KEY.encode('utf-8'))
    # 填充要加密的数据
    h.update(str(content).encode('utf-8'))
    if confusion:
        h.update(str(confusion).encode('utf-8'))
    # 获取加密结果
    return h.hexdigest()


# 正则判断
def judge_type(account):
    phone = r"(^[1]([3-9])[0-9]{9}$)"
    email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    try:
        if re.match(phone, account):
            return 'phone'
        else:
            return 'email' if re.match(email, account) else None
    # 前端直接传null时返回None
    except TypeError:
        return None


# 短信
def send_sms(phone, checkcode):
    client = AcsClient(settings.ACCESS_KEYID, settings.ACCESS_SECRET, 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "KingNetwork")
    request.add_query_param('TemplateCode', "SMS_174986857")
    request.add_query_param('TemplateParam', "{\"code\":\"%s\"}" % checkcode)

    response = client.do_action(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))
    response = json.loads(response)
    return 'OK' if response['Message'] == "OK" else response['Message']


class UserTourView(View):
    def get(self, request, user_id):
        # 获取用户历史游览记录
        # default为setting中的redis配置的default信息
        con = get_redis_connection('default')
        # 储存的用户id键
        history_key = 'history_%d' % user_id
        # 获取用户最新游览的30个商品id
        goods_ids = con.lrange(history_key, 0, 30)
        # 客户游览的商品顺序最新的在最左边，拿出来的顺序才是对的
        # 所以不能乱，遍历用户游览的商品从数据库中查询商品
        # 获取用户游览的商品信息
        # goods_li = []
        # for goods in goods_ids:
        #     # goods = Goods.objects.get(id=goods_id)
        #     goods_li.append(goods)

        # 序列化  这时使用eval()对获取的结果转换成dict
        # goods_ids = eval(goods_ids)
        data = json.loads(serialize("json", goods_ids))
        return JsonResponse({'goods': data})

    def post(self, request):
        """游览记录post"""
        # json解析
        r = json.loads(request.body)
        # 获取传过来的user_id
        user_id = r['user_id']
        goods_id = r['goods_id']
        # 获取用户历史游览记录
        # default为setting中的redis配置的default信息
        con = get_redis_connection('default')
        # 储存的用户id键
        history_key = 'history_%d' % user_id
        # lpush(name, values)：在name对应的list中添加元素，每个新的元素都添加到列表的最左边
        # rpush(name, values)：在name对应的list中添加元素，每个新的元素都添加到列表的最右边
        # lrange(name, start, end)：在name列表中分片获取数据，start为索引的起始位置，end为索引结束位置
        # 往左边添加数据
        goods_obj = Goods.objects.get(id=goods_id)
        con.lpush(history_key, goods_obj)
