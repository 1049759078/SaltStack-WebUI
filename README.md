# SaltStack-WebUI
### 组件版本和运行环境
Mac OS X   Python 3.5.2   Django 1.10   Bootstrap 4.0</br>
admin使用了<a href="https://github.com/geex-arts/django-jet">django-jet</a></br>
分页插件使用了<a href="https://github.com/jamespacileo/django-pure-pagination">django-pure-pagination</a>
### 部署步骤
1. 新建mysql数据库,在setting.py文件的DATABASES中可设置数据库连接信息</br>
2. 同步数据库</br>
<code>
$ python manage.py makemigrations</br>
$ python manage.py migrate
</code></br>
3. 在saltapi目录下的saltAPI.py中配置saltapi的地址端口、用户名、密码
### 功能实现
C9B2C63E-FDB3-428E-BA1D-4465EAA8BADE.png
753A58FA-356A-4BD9-8A83-B36A88FD0986.png
