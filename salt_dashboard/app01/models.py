from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Module(models.Model):
    client = models.CharField(u'Salt模块类型', max_length=20, default='execution')
    name = models.CharField(u'Salt模块名称', max_length=20)
    def __str__(self):
        return "%s - %s"% (self.client,self.name)
    class Meta:
        verbose_name = u'Salt模块'
        verbose_name_plural = u'Salt模块列表'
        unique_together = ("client", "name")

class Command(models.Model):
    cmd = models.CharField(u'Salt命令', max_length=100)
    doc = models.TextField(u'帮助文档', max_length=1000, blank=True, null=True)
    module = models.ForeignKey('Module', verbose_name=u'所属模块')
    def __str__(self):
        return  u"%s - %s"%(self.module,self.cmd)
    class Meta:
        verbose_name = u'Salt命令'
        verbose_name_plural = u'Salt命令列表'
        unique_together = ("module", "cmd")

class Minions(models.Model):
    Status = (
    ('Unknown', 'Unknown'),
    ('Accepted', 'Accepted'),
    ('Denied', 'Denied'),
    ('Unaccepted', 'Unaccepted'),
    ('Rejected', 'Rejected'),
    )
    minion = models.CharField(u'客户端', max_length=50, unique=True)
    grains = models.TextField(u'Grains信息', max_length=500, blank=True)
    pillar = models.TextField(u'Pillar信息', max_length=500, blank=True)
    status = models.CharField(u'在线状态', choices=Status, max_length=20, default='Unknown')
    def __str__(self):
        return self.minion
    class Meta:
        verbose_name = u'Salt客户端'
        verbose_name_plural = u'Salt客户端列表'

class Result(models.Model):
    #命令
    client = models.CharField(u'执行方式', max_length=20, blank=True)
    fun = models.CharField(u'命令', max_length=50)
    arg = models.CharField(u'参数', max_length=255, blank=True)
    tgt_type =  models.CharField(u'目标类型', max_length=20)
    #返回
    jid = models.CharField(u'任务号', blank=True, max_length=50)
    minions = models.CharField(u'目标主机', max_length=500, blank=True)
    result = models.TextField(u'返回结果', blank=True)
    #其他信息
    user = models.CharField(u'操作用户', max_length=50)
    datetime =models.DateTimeField(u'执行时间', auto_now_add=True)
    def __str__(self):
        return self.jid
    class Meta:
        verbose_name = u'命令返回结果'
        verbose_name_plural = u'命令返回结果'
