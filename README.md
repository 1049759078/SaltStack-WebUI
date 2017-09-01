# SaltStack-WebUI
### 组件版本和运行环境
Mac OS X   Python 3.5.2   Django 1.10   Bootstrap 4.0</br>
admin使用了<a href="https://github.com/geex-arts/django-jet">django-jet</a></br>
分页插件使用了<a href="https://github.com/jamespacileo/django-pure-pagination">django-pure-pagination</a>
### 部署步骤
1.新建mysql数据库,在setting.py文件的DATABASES中可设置数据库连接信息
2.同步数据库
'''
$ python manage.py makemigrations
$ python manage.py migrate
'''
3.在saltapi目录下的saltAPI.py中配置saltapi的地址端口、用户名、密码
### 功能实现
