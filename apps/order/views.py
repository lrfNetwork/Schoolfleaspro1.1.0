import datetime
import json
import os

from alipay import AliPay
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django_redis import get_redis_connection, cache

from apps import user
from apps.goods.models import Goods
from apps.order.models import OrderInfo
from django.conf import settings


class OrderCommitView(View):
    @transaction.atomic
    def post(self, request):
        """订单创建"""
        # 前端传递的参数:商品id(goods_id)
        r = json.loads(request.body)
        user_id = r['user_id']
        goods_ids = r['goods_id']

        # 设置事务保存点
        save_id = transaction.savepoint()

        # 接收参数
        for goods_id in goods_ids:
            try:
                good = Goods.objects.get(id=goods_id)
                # 获取库存
                stockgood = good.stock
            except Goods.DoesNotExist:
                # 事务回滚
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'success': bool(False), 'msg': "该商品不存在！"})
            # 组织参数
            # 订单num: 20171122181630+用户id
            order_num = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
            try:
                # todo: 向schoolfleaspro_order_info表中添加一条记录
                order = OrderInfo.objects.create(order_num=order_num,
                                                 username=user_id,
                                                 # pay_method=pay_method,
                                                 total_count=1,
                                                 total_price=goods_id.price,
                                                 transit_price=goods_id.express)
                # 缓存数据库存
                # 暂时不修改数据库数据，防止同时下单，以及下单失败

                goods_stock = 'stock_%d' % goods_id
                # 判断是否存在缓存
                if not cache.hexists(goods_stock):
                    # 订单缓存保留30分钟，
                    cache.hset('goods_stock', stockgood - 1, 30 * 60)

                # 订单缓存保留30分钟，
                # 获取库存
                stockcount = cache.hget('goods_stock')
                if stockcount is None:
                    # 事务回滚
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'success': bool(False), 'msg': "库存不足！"})
                else:
                    # 更新库存
                    cache.hset('goods_stock', stockcount - 1, 30 * 60)
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'success': bool(False), 'msg': "下单失败，请重试！"})
        # 下单成功
        return JsonResponse({'success': bool(True), 'msg': "成功"})


class OrderPayView(View):
    def get(self, request):
        pass

    def post(self, request):

        # 前端传递的参数:订单id(order_id)
        r = json.loads(request.body)
        order_id = r['order_id']
        paymethod = r['paymethod']

        # 校验参数
        if not all([order_id]):
            return JsonResponse({'success': bool(False), 'msg': "提交参数不完整！"})

        try:
            order = OrderInfo.objects.get(id=order_id,
                                          # pay_method=3,  # alipay
                                          order_status=1)  # 待支付状态
        except OrderInfo.DoesNotExist:
            return JsonResponse({'success': bool(False), 'msg': "订单错误！"})

        # 由于之前没有选择支付方式现在需要保存支付方式
        order.pay_method = paymethod
        order.save()
        # 判断支付方式
        # 支付宝
        if paymethod == 3:
            # 业务处理:使用python sdk调用支付宝的支付接口
            # 初始化
            alipay = AliPay(
                appid="2016101300676030",  # 应用id
                app_notify_url=None,  # 默认回调url
                app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipaykey/app_private_key.pem'),
                alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipaykey/alipay_public_key.pem'),
                # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                sign_type="RSA2",  # RSA 或者 RSA2
                debug=True  # 默认False  部署需要修改为False
            )

            # 调用支付接口
            # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
            total_pay = order.total_price + order.transit_price  # Decimal
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=order.order_num,  # 订单num
                # Decimal类型的数据不能被序列化，必须先转化为str
                total_amount=str(total_pay),  # 支付总金额
                subject='SchoolFleas校园跳蚤%s' % order_id,
                return_url=None,  # 通知地址，调式阶段为None,部署改为回调地址即可
                notify_url=None  # 可选, 不填则使用默认notify url
            )

            # 返回应答
            # 返回支付链接
            pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
            content = {
                'success': bool(True),
                'pay_method': 3,
                'pay_url': pay_url
            }
            return JsonResponse(content)
        elif paymethod == 0:
            # 货到付款
            content = {
                'success': bool(True),
                'pay_method': 1,
                'pay_url': ''  # 不需要支付
            }
            return JsonResponse(content)


class CheckPayView(View):
    """查看订单支付结果"""

    def post(self, request):
        # 前端传递的参数:订单id(order_id)
        r = json.loads(request.body)
        order_id = r['order_id']
        # 校验参数
        if not all([order_id]):
            return JsonResponse({'success': bool(False), 'msg': "提交参数不完整！"})

        try:
            order = OrderInfo.objects.get(id=order_id,
                                          # pay_method=3,  # alipay
                                          order_status=1)  # 待支付状态
        except OrderInfo.DoesNotExist:
            return JsonResponse({'success': bool(False), 'msg': "订单错误！"})

        # 业务处理:使用python sdk调用支付宝的支付接口
        # 初始化
        alipay = AliPay(
            appid="2016101300676030",  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipaykey/app_private_key.pem'),
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/order/alipaykey/alipay_public_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False  部署需要修改为False
        )

        # 调用支付宝的交易查询接口
        while True:
            response = alipay.api_alipay_trade_query(order.order_num)

            # response = {
            #         "trade_no": "2017032121001004070200176844", # 支付宝交易号
            #         "code": "10000", # 接口调用是否成功
            #         "invoice_amount": "20.00",
            #         "open_id": "20880072506750308812798160715407",
            #         "fund_bill_list": [
            #             {
            #                 "amount": "20.00",
            #                 "fund_channel": "ALIPAYACCOUNT"
            #             }
            #         ],
            #         "buyer_logon_id": "csq***@sandbox.com",
            #         "send_pay_date": "2017-03-21 13:29:17",
            #         "receipt_amount": "20.00",
            #         "out_trade_no": "out_trade_no15",
            #         "buyer_pay_amount": "20.00",
            #         "buyer_user_id": "2088102169481075",
            #         "msg": "Success",
            #         "point_amount": "0.00",
            #         "trade_status": "TRADE_SUCCESS", # 支付结果
            #         "total_amount": "20.00"
            # }
            code = response.get('code')
            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 获取支付宝交易号
                trade_no = response.get('trade_no')
                # 更新订单状态
                order.trade_no = trade_no
                order.order_status = 2  # 代发货
                order.save()
                # 返回结果
                return JsonResponse({'res': 3, 'message': '支付成功'})
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                # 等待买家付款
                # 业务处理失败，可能一会就会成功
                import time
                time.sleep(5)
                continue
            else:
                # 支付出错
                print(code)
                return JsonResponse({'success': bool(False), 'msg': "支付失败！"})
