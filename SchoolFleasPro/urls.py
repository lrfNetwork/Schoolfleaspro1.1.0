from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.views.static import serve
from SchoolFleasPro.settings import MEDIA_ROOT
from apps.goods.views import goodsdata,log

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^user/', include(('user.urls', 'user'), namespace='user')),  # 用户模块URL
    url(r'^goods/', include(('goods.urls', 'goods'), namespace='goods')),  # 商品模块URL
    path('collect/', include(('collect.urls', 'collect'), namespace='collect')),  # 收藏夹
    # 添加DjangoUeditor的URL
    url(r'^ueditor/', include('DjangoUeditor.urls')),

    # 文件上传url指向
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    url(r'admin/goods/data', goodsdata),
    url(r'admin/user/log', log),
]
