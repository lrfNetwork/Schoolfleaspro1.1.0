# -*- coding: utf-8 -*-
# @Time    : 10/6/2019 1:03 PM
# @Author  : JIN Wenjie
# @FileName: views.py
# @Software: PyCharm
# @Blog    : https://jinwenjie.me

# 导入View抽象类post,get方法
from django.shortcuts import render
from django.views.generic import View
from apps.goods.models import Goods
from django.http import JsonResponse
from apps.user.models import User
# 分页
from django.core.paginator import Paginator
import json


# Create your views here.

# 首页商品游览
class GoodsMainView(View):
    # 步长
    STEP = 6

    def get(self, request):
        pass

    def post(self, request):
        r = json.loads(request.body)
        category = r['category']
        page = r['page']
        try:
            if category == '最新':
                goods_list = Goods.objects.all().order_by("-id")
            else:
                goods_list = Goods.objects.filter(category=category).order_by("-id")
            p = Paginator(goods_list, GoodsMainView.STEP)
            if p.num_pages >= page:
                goods_page = p.page(page)
            else:
                return JsonResponse({'data': None})
            # 将查询到的数据发送给前端
            goods = []
            for item in goods_page:
                goods.append({
                    'id': item.id,
                    'title': item.title,
                    'price': item.price,
                    # 只获取第一张图片展示
                    'url': item.url.split('|', 1)[0]
                })
            return JsonResponse({'data': goods})
        except Goods.DoesNotExist:
            return JsonResponse({'data': None})


# 商品详情页
class GoodsDetailView(View):
    def get(self, request):
        pass

    def post(self, request):
        r = json.loads(request.body)
        goods_id = r['id']
        try:
            goods = Goods.objects.get(id=goods_id)
            # 获取卖家名
            try:
                seller_name = User.objects.get(id=goods.seller_id).username
            except User.DoesNotExist:
                return JsonResponse({'success': bool(False)})
            # 分割图片url
            url = goods.url.split('|')
            return JsonResponse({
                'title': goods.title,
                'detail': goods.detail,
                'url': url,
                'price': goods.price,
                'express': goods.express,
                'sellerId': goods.seller_id,
                'sellerName': seller_name,
                'area': goods.area
            })
        except Goods.DoesNotExist:
            return JsonResponse({'success': bool(False)})


# 商品搜索
class GoodsSearchView(View):
    # 步长
    STEP = 6

    def get(self, request):
        pass

    def post(self, request):
        r = json.loads(request.body)
        title = r['title']
        try:
            goods_list = Goods.objects.filter(title__icontains=title).order_by("-id")
            # 将查询到的数据发送给前端
            goods = []
            for item in goods_list:
                goods.append({
                    'id': item.id,
                    'title': item.title,
                    'price': item.price,
                    # 只获取第一张图片展示
                    'url': item.url.split('|', 1)[0]
                })
            return JsonResponse({'data': goods})
        except Goods.DoesNotExist:
            return JsonResponse({'data': None})


# 商品上传
class GoodsUploadView(View):
    def get(self, request):
        pass

    def post(self, request):
        r = json.loads(request.body)
        title = r['title']
        detail = r['detail']
        category = r['category']
        # {url: url1, hash: hash1}
        # url通过 | 分割多个图片链接存在一个字段，hash同理
        url_array = r['url']
        seller_id = r['sellerId']
        price = r['price']
        express = r['express']
        area = r['area']
        url = ''
        for item in url_array:
            url = url + str(item['url']) + '|'
        img_hash = ''
        for item in url_array:
            img_hash = img_hash + str(item['hash']) + '|'
        goods = Goods()
        goods.status = 2
        goods.title = title
        goods.detail = detail
        goods.category = category
        # 去除最后多余的|
        goods.url = url[:-1]
        goods.img_hash = img_hash[:-1]
        goods.seller_id = seller_id
        goods.price = price
        goods.express = express
        # 去除最后多余的,
        goods.area = area[:-1]
        goods.save()
        return JsonResponse({'success': bool(True)})


# 商品推荐页
class GoodsRecommendView(View):
    def get(self, request):
        pass

    def post(self, request):
        print(request)


def goodsdata(request):
    context = {'hello': 'Hello World!'}
    return render(request, 'admin/showdata1.html', context)


def log(request):
    return render(request, 'admin/userlog.html')
