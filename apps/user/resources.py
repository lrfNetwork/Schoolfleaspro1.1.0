from import_export import resources
from .models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User


'''调用直接用下面的方法'''
# from .resources import UserResource
# user_resource = UserResource()
# dataset = user_resource.export()

# 导出数据到CSV
# dataset.csv

# 导出数据到JSON
# dataset.json

# 导出数据到YAML
# dataset.yaml
