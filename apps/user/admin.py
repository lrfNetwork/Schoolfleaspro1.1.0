from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from utils.MiXin import ExportExcelMixin
from .models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin, ExportExcelMixin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = (
        'id', 'username', 'email', 'phone', 'headimage_data', 'create_time', 'last_login', 'Blacklist', 'buttons')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)

    # list_filter = []
    # 搜索框
    search_fields = ('username', 'phone')

    # 设置可编辑
    list_editable = ['Blacklist']

    # 筛选器
    list_filter = ('Blacklist', 'create_time')

    actions = ['pullblacklist', 'pulloutblacklist', 'theblacklist', 'BlackList', 'export_as_excel']

    # 一键拉入黑名单
    def pullblacklist(self, request, queryset):  # 具体的导出方法的实现
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        User.objects.filter(id__in=selected).update(Blacklist=1)

    pullblacklist.short_description = '批量拉黑'  # 该动作在admin中的显示文字
    # export_as_excel.style = "color:red;"
    pullblacklist.type = 'danger'

    # 一键拉出黑名单
    def pulloutblacklist(self, request, queryset):  # 具体的导出方法的实现
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        User.objects.filter(id__in=selected).update(Blacklist=0)

    pulloutblacklist.short_description = '一键拉出'  # 该动作在admin中的显示文字
    pulloutblacklist.type = 'success'

    # 添加编辑
    def buttons(self, obj):
        button_html = """<a class="changelink" href="/admin/user/user/%s/change/">编辑</a>""" % (
            obj.id)
        return format_html(button_html)

    buttons.short_description = "操作"

    # 头像展示
    def headimage_data(self, obj):
        try:
            img = mark_safe(u'<img src="%s" width="100px" />' % (obj.headimg.url,))
        except Exception as e:
            img = ''
        return img

    headimage_data.short_description = '头像'
