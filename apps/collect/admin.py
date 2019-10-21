from django.contrib import admin
from utils.MiXin import ExportExcelMixin
from apps.collect.models import Collect, ShopCart


# Register your models here.

@admin.register(Collect)
class collectAdmin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ['id', ]
