from decimal import Decimal
from django.db import models
from django.utils.html import format_html

from db.base_model import BaseModel
from DjangoUeditor.models import UEditorField


# Create your models here.
class GoodsCategory(BaseModel):
    """商品分类"""
    category = models.CharField(max_length=20, default='', verbose_name='商品类型')

    class Meta:
        db_table = 'SchoolFleasPro_category'
        verbose_name = '商品分类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category


class Goods(BaseModel):
    """商品类模型"""
    STATUS_CHOICE = (
        (0, '下架'),
        (1, '上架'),
        (2, '待审核'),
    )
    status = models.IntegerField(default=2, choices=STATUS_CHOICE, verbose_name='商品状态')
    title = models.CharField(max_length=40, default='', verbose_name='商品标题')
    detail = models.TextField(default='', verbose_name='商品详情')
    category = models.ForeignKey('GoodsCategory', default='', verbose_name='商品类型', on_delete=models.CASCADE)
    url = models.TextField(default='', verbose_name='商品图片链接')
    img_hash = models.TextField(default='', verbose_name='商品图片hash')
    seller = models.ForeignKey('user.User', default='', verbose_name='卖家账户', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='商品价格')
    express = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='商品运费')
    area = models.CharField(max_length=20, default='', verbose_name='发货地')
    stock = models.IntegerField(default=1, verbose_name='库存')
    Introduction = UEditorField(default='', verbose_name='商品介绍', width=800, height=500,
                                toolbars="full", imagePath="upimg/", filePath="upfile/",
                                upload_settings={"imageMaxSize": 1204000},
                                settings={}, command=None, blank=True)
    color_code = models.CharField(max_length=6, verbose_name='颜色', default='green')

    class Meta:
        db_table = 'SchoolFleasPro_Goods'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name

    def __int__(self):
        return self.category


class RecommendGoods(BaseModel):
    goods_name = models.ForeignKey('Goods', verbose_name='商品名称', on_delete=models.CASCADE)

    class Meta:
        db_table = 'SchoolFleasPro_RecommendGoods'
        verbose_name = '推荐商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods_name
