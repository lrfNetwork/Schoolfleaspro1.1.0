from django.conf.urls import url
from apps.goods.views import GoodsMainView, GoodsUploadView, GoodsDetailView, GoodsSearchView

urlpatterns = [
    url(r'^browse$', GoodsMainView.as_view(), name='goodsBrowse'),
    url(r'^detail$', GoodsDetailView.as_view(), name='goodsDetail'),
    url(r'^search$', GoodsSearchView.as_view(), name='goodsSearch'),
    url(r'^browse$', GoodsMainView.as_view(), name='goodsBrowse'),
    url(r'^upload$', GoodsUploadView.as_view(), name='goodsUpload'),

]
