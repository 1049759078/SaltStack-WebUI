# SaltStack-WebUI
### 组件版本和运行环境
Mac OS X   Python 3.5.2   Django 1.10   Bootstrap 4.0</br>
admin使用了<a href="https://github.com/geex-arts/django-jet">django-jet</a></br>
分页插件使用了<a href="https://github.com/jamespacileo/django-pure-pagination">django-pure-pagination</a>
### 部署步骤
1. 新建mysql数据库,在setting.py文件的DATABASES中可设置数据库连接信息</br>
2. 同步数据库<code>$ python manage.py makemigrations   $ python manage.py migrate</code></br>
3. 在saltapi目录下的saltAPI.py中配置saltapi的地址端口、用户名、密码
### 功能实现
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/C9B2C63E-FDB3-428E-BA1D-4465EAA8BADE.png)
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/753A58FA-356A-4BD9-8A83-B36A88FD0986.png)
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/929B5F40-8EE9-436B-A208-E5DA72512B42.png)
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/C919C2F1-A553-49B7-BE93-39C48E6C845D.png)
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/E789357E-3E8B-445E-9820-95D782A4C211.png)
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/E8A0DB18-5924-48BC-A660-3134CBF9D7E3.png)
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/4E6591B6-42BD-40C8-BDB3-0E36BD91C8BC.png)
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/B3405090-4123-42F6-B977-26351824BBFA.png)
![image](https://github.com/RickyLin7/SaltStack-WebUI/blob/New_Branch01/salt_dashboard/static/img/F585A0DB-F3F8-4F00-9627-CC57FD4AC72F.png)
