from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from utils.MiXin import ExportExcelMixin
from .models import Goods, GoodsCategory
from apps.user.models import User
# Excel导出
from openpyxl import Workbook

admin.site.site_title = 'SchoolFleas管理系统'
admin.site.site_header = 'SchoolFleas管理系统'


# Register your models here.


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin, ExportExcelMixin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'title', 'getCategory', 'price', 'getUserphone', 'create_time', 'status', 'buttons')
    list_filter = [ 'status','create_time',]
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
    # 搜索框
    search_fields = ('title',)
    # 设置可编辑
    list_editable = ('status',)
    # 设置可编辑
    # list_display_links = ('title',)
    date_hierarchy = 'create_time'

    # List_display_links = True
    # actions_on_top = True
    # fields = ['category']

    # fk_fields = ('seller_phone',)
    # def has_add_permission(self, request):
    #     return True
    # list_filter = ('id',)
    def getUserphone(self, obj):
        return obj.seller.phone

    # 重命名
    getUserphone.short_description = u'卖家电话'

    def getCategory(self, obj):
        return obj.category.category

    # 重命名
    getCategory.short_description = u'商品类别'

    # # 增加自定义按钮
    # actions = ['make_copy', 'custom_button']
    #
    # def custom_button(self, request, queryset):
    #     pass

    # 编辑
    def buttons(self, obj):
        button_html = """<a class="changelink" href="/admin/goods/goods/%s/change/">编辑</a>""" % (
            obj.id)
        return format_html(button_html)

    buttons.short_description = "操作"

    actions = ['export_as_excel', 'fastShelves', 'fastunShelves']  # 增加动作, 对应相应的方法名

    # 一键下架
    def fastunShelves(self, request, queryset):  # 具体的导出方法的实现
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        Goods.objects.filter(id__in=selected).update(status=0)

    fastunShelves.short_description = '一键下架'  # 该动作在admin中的显示文字
    # export_as_excel.style = "color:red;"
    fastunShelves.type = 'danger'

    # 一键上架
    def fastShelves(self, request, queryset):  # 具体的导出方法的实现
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        Goods.objects.filter(id__in=selected).update(status=1)

    fastShelves.short_description = '一键上架'  # 该动作在admin中的显示文字
    # export_as_excel.style = "color:red;"
    fastShelves.type = 'success'

    date_hierarchy = 'create_time'


@admin.register(GoodsCategory)
class CategoryAdmin(admin.ModelAdmin, ExportExcelMixin):
    # prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'category', 'buttons')

    def __str__(self):
        return self.name

    # 添加编辑链接
    def buttons(self, obj):
        button_html = """<a class="changelink" href="/admin/goods/goodscategory/%s/change/">编辑</a>""" % (
            obj.id)
        return format_html(button_html)

    buttons.short_description = "操作"

    # Excel导出
    actions = ['export_as_excel']
    # 设置可编辑
    # list_display_links = ('category',)

    # list_filter = ['category']
    # 搜索框
    search_fields = ('title',)