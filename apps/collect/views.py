import json
from typing import Dict, Any

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from apps.collect.models import Collect, ShopCart


def search(request):

    data = []
    if request.method == "GET":
        return HttpResponse("不接受get方法！")
    elif request.method == "POST":
        # 获取传来的json信息
        r = json.loads(request.body)
        goodsID = r['goodsId']
        userId = r['userId']
        judgeType = r['type']
        # 收藏表
        if judgeType == 1:
            # 为空时返回收藏列表
            if goodsID is None:
                # 获取到该用户的收藏的商品
                collects = Collect.objects.filter(user_id=userId)
                # start
                ary = []
                for item in collects:
                    goods = item.goods
                    # 序列化必须是可迭代对象哦！所以加入到数组里面
                    ary.append(goods)
                data = json.loads(serialize("json", ary))
                # end
                return JsonResponse({"goods": data})
            # 不为空时查询收藏
            elif goodsID is not None:
                collects = Collect.objects.get(user_id=userId,goods_id=goodsID)
                # start
                ary = []
                ary.append(collects.goods)
                data = serialize("json", ary)
                # 解决中文编码问题
                data=json.loads(data)
                # end
                return JsonResponse({"goods": data})

        # 购物车表
        elif judgeType == 2:
            shopCarts = ShopCart.objects.filter(user_id=userId)
            ary = []
            for item in shopCarts:
                goods = item.goods
                # 序列化必须是可迭代对象哦！所以加入到数组里面
                ary.append(goods)
            data = json.loads(serialize("json", ary))
            return JsonResponse({"goods": data})
        else:
            # 处理错误信息
            return HttpResponse("error")


def index(request):
    return render(request, 'test.html')
