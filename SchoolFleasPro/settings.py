import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+#8by3l3ay^l^1iw%#iwre_j+f(d63^)wdi+y#y#5p1#k=roq*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 将apps添加到python搜索路径中
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',  # 导入simpleui'
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.user',  # 注册user模块
    'apps.order',  # 订单order模块
    'apps.goods',  # 商品goods模块
    'apps.collect',  # 商品collect模块
    'corsheaders',  # 跨域问题
    'import_export',  # 数据库格式转换插件
    'DjangoUeditor',  # 富文本
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域
]

ROOT_URLCONF = 'SchoolFleasPro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 设置模板路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SchoolFleasPro.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schoolfleaspro',
        'USER': 'schoolfleaspro',
        'PASSWORD': 'schoolfleaspro',
        'HOST': 'localhost',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# 静态文件路径
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
# 设置文件上传路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# 发送短信AK
ACCESS_KEYID = 'LTAI4FebqBNi9DQup4L3AdM3'
ACCESS_SECRET = 'O7TsRfUn5kKxoX8U5SWDkXR9eILss3'

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smpt服务地址
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'schoolfleas@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'lrf15883723040'
# 收件人看到的发件人
EMAIL_FROM = '校园跳蚤<schoolfleas@163.com>'

# 设置redis缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 设置缓存存储session，此时mysql中的django_session将不再存储session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 与CACHES中的default对应
SESSION_CACHE_ALIAS = "default"
# session在cookie中的保存时间
SESSION_COOKIE_AGE = 60 * 30
# 设置session在浏览器关闭时过期
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 跨域
CORS_ORIGIN_ALLOW_ALL = True

# 设置Django的文件存储类
# 关闭则不开启fastdfs
# DEFAULT_FILE_STORAGE = 'utils.fdfs.storage.FDFSStorage'

# 设置fdfs使用的client.conf文件路径
FDFS_CLIENT_CONF = './utils/fdfs/client.conf'

# 设置fdfs存储服务器上nginx的IP和端口号
FDFS_URL = 'http://172.16.179.131:8888/'

# 首页配置
# SIMPLEUI_HOME_PAGE = 'goods/data'

# 首页标题
SIMPLEUI_HOME_TITLE = '首页'
# 首页图标
SIMPLEUI_HOME_ICON = 'fas fa-paper-plane'

SIMPLEUI_HOME_INFO = False

# 最近操作信息
SIMPLEUI_HOME_ACTION = True

IMPORT_EXPORT_USE_TRANSACTIONS = True

#
#
# admin.site.site_header = 'SchoolFleas管理系统'
#
# admin.site.site_title = 'SchoolFleas管理系统'


# VERBOSE_APP_NAME = "SchoolFleas管理系统"

SIMPLEUI_STATIC_OFFLINE = False

SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['商品管理', '用户管理', ],  # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [{
        'name': '商品管理',
        'icon': 'fas el-icon-goods',
        'models': [{
            'name': '商品分类',
            'icon': 'fa fa-cart-plus',
            'url': 'goods/goods'
        }, {
            'name': '商品列表',
            'icon': 'fa el-icon-s-unfold',
            'url': 'goods/goods'
        }]
    }, {
        'name': '用户管理',
        'icon': 'fas fa-user-shield',
        'models': [{
            'name': '用户中心',
            'icon': 'fa fa-user',
            'url': 'user/user'
        }, {
            'name': '数据统计',
            'icon': 'fa fa-user',
            'url': 'goods/data'
        }, {
            'name': '用户log',
            'icon': 'fa fa-user',
            'url': 'user/log'
        }]
    }]
}

# 指定simpleui默认的主题,指定一个文件名，相对路径就从simpleui的theme目录读取
SIMPLEUI_DEFAULT_THEME = 'e-red-pro.css'
