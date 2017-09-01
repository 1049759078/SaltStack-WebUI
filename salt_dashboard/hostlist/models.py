from django.db import models
# Create your models here.

class IdcAsset(models.Model):
    IdcType = (
        ('DX', u'电信'),
        ('LT', u'联通'),
        ('YD', u'移动'),
        ('ZJ', u'自建'),
    )
    idc_name = models.CharField(u'机房名称', max_length=20, unique=True)
    idc_operators = models.CharField(u'运营商', choices=IdcType, max_length=20, default='DX')
    idc_location = models.CharField(u'机房地址', max_length=30, blank=True)
    idc_contacts = models.CharField(u'联系电话', max_length=30, blank=True)
    remark = models.TextField(u'备注', max_length=50, blank=True, default='')

    def __str__(self):
        return self.idc_name

    class Meta:
        verbose_name = u'IDC资产信息'
        verbose_name_plural = u'IDC资产信息管理'

class Maintainer(models.Model):
    username = models.CharField(max_length=30, blank=True, verbose_name=u'维护人员')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = u'维护人员'
        verbose_name_plural = u'维护人员列表'

class HostList(models.Model):
    ip = models.OneToOneField('HostAsset', unique=True, verbose_name=u'IP地址')
    status = models.BooleanField(default=True, verbose_name=u'使用状态')
    idc = models.ForeignKey('IdcAsset', null=True, blank=True, verbose_name=u'所属机房')
    maintainer = models.ForeignKey('Maintainer', null=True, blank=True, verbose_name=u'维护人员')
    def __str__(self):
        return self.ip.ip
    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u'主机列表'

class HostAsset(models.Model):
    ip = models.GenericIPAddressField(u'IP地址', unique=True)
    hostname = models.CharField(u'主机名', max_length=30, blank=True)
    fqdn = models.CharField(u'计算机全称', max_length=50, blank=True)
    domain = models.CharField(u'域名', max_length=50, blank=True)
    macaddress = models.CharField(u'MAC地址', max_length=40, blank=True)
    os = models.CharField(u'操作系统', max_length=50, blank=True)
    osarch = models.CharField(u'系统架构', max_length=50, blank=True)
    osrelease = models.CharField(u'系统版本', max_length=50, blank=True)
    manufacturer = models.CharField(u'厂商', max_length=20, blank=True)
    productname = models.CharField(u'产品型号', max_length=30, blank=True)
    serialnumber = models.CharField(u'序列号', max_length=80, blank=True)
    cpu_model = models.CharField(u'CPU型号', max_length=50, blank=True)
    cpu_nums = models.PositiveSmallIntegerField(u'CPU线程数', blank=True)
    cpu_groups = models.PositiveSmallIntegerField(u'CPU物理核数', blank=True)
    mem = models.CharField(u'内存大小', max_length=5, blank=True)
    virtual = models.CharField(u'虚拟环境', max_length=20, blank=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = u'主机资产信息'
        verbose_name_plural = u'主机资产信息管理'
