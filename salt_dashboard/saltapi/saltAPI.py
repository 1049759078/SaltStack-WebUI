#!/usr/bin/env python3
#coding=utf-8

import urllib.request, urllib.parse, json, re

import ssl
context = ssl._create_unverified_context()

class saltAPI:
    def __init__(self):
        self.__url = ''          #salt-api监控的地址和端口如:'https://192.168.1.100:8080'
        self.__user =  ''        #salt-api用户名
        self.__password = ''     #salt-api用户密码
        self.__token_id = self.salt_login()

    def salt_login(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.parse.urlencode(params).encode(encoding='UTF8')
        headers = {'X-Auth-Token':''}
        url = self.__url + '/login'
        req = urllib.request.Request(url, encode, headers)
        opener = urllib.request.urlopen(req, context=context)
        content = json.loads(opener.read().decode('utf8'))
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError

    def postRequest(self, obj, prefix='/'):
        headers = {'X-Auth-Token': self.__token_id}
        url = self.__url + prefix
        if obj:
            data, number = re.subn(b"arg\d*", b'arg', obj)
        else:
            data=None
        req = urllib.request.Request(url, obj, headers)
        opener = urllib.request.urlopen(req, context=context)
        #print(opener)
        content = json.loads(opener.read().decode('utf8'))
        return content

    # def saltCmd(self, params):
    #     obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
    #     obj, number = re.subn(b'arg\d', b'arg', obj)
    #     res = self.postRequest(obj)
    #     return res

    #执行命令
    def SaltCmd(self,tgt,fun,client='local_async',expr_form='glob',arg=None,**kwargs):
        params = {'client':client, 'fun':fun, 'tgt':tgt, 'expr_form':expr_form}
        if arg:
            a=arg.split(',') #参数按逗号分隔
            for i in a:
                b=i.split('=') #每个参数再按=号分隔
                if len(b)>1:
                    params[b[0]]='='.join(b[1:]) #带=号的参数作为字典传入
                else:
                    params['arg%s'%(a.index(i)+100)]=i
        if kwargs:
            params=dict(list(params.items())+list(kwargs.items()))
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        ret = self.postRequest(obj)
        return ret

    def SaltRun(self,fun,client='runner_async',arg=None,**kwargs):
        params = {'client':client, 'fun':fun}
        if arg:
            a=arg.split(',') #参数按逗号分隔
            for i in a:
                b=i.split('=') #每个参数再按=号分隔
                if len(b)>1:
                    params[b[0]]='='.join(b[1:]) #带=号的参数作为字典传入
                else:
                    params['arg%s'%a.index(i)]=i
        if kwargs:
            params=dict(list(params.items())+list(kwargs.items()))
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        ret = self.postRequest(obj)
        return ret

    def list_all_key(self):
        prefix = '/keys'
        content = self.postRequest(None,prefix)
        accepted = content['return']['minions']
        denied = content['return']['minions_denied']
        unaccept = content['return']['minions_pre']
        rejected = content['return']['minions_rejected']
        return accepted, denied, unaccept, rejected

    # def list_all_key(self):
    #     params = {'client': 'wheel', 'fun': 'key.list_all'}
    #     obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
    #     content = self.postRequest(obj)
    #     minions = content['return'][0]['data']['return']['minions']
    #     minions_pre = content['return'][0]['data']['return']['minions_pre']
    #     #minions_rej = content['return'][0]['data']['return']['minions_rejected']
    #     return minions, minions_pre

    # def actionKeys(self, node_name, action):
    #     '''
    #     对Minion keys 进行指定处理,如接受、拒绝、删除；
    #     '''
    #     func = 'key.' + action
    #     params = {'client': 'wheel', 'fun': func, 'match': node_name}
    #     obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
    #     content = self.postRequest(obj)
    #     ret = content['return'][0]['data']['success']
    #     return ret

    # def accept_key(self,node_name):
    #     params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
    #     obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
    #     content = self.postRequest(obj)
    #     ret = content['return'][0]['data']['success']
    #     return ret

    # def delete_key(self,node_name):
    #     params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
    #     obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
    #     content = self.postRequest(obj)
    #     ret = content['return'][0]['data']['success']
    #     return ret

    #获取grains
    def SaltMinions(self,minion=''):
        if minion and minion!='*':
            prefix = '/minions/'+minion
        else:
            prefix = '/minions'
        ret = self.postRequest(None,prefix)
        return ret

    #获取job id的详细执行结果
    def SaltJob(self,jid=''):
        if jid:
            prefix = '/jobs/'+jid
        else:
            prefix = '/jobs'
        ret = self.postRequest(None,prefix)
        return ret

    # def SaltJob(self,jid):
    #     params = {'client':'runner', 'fun':'jobs.lookup_jid', 'jid':jid}
    #     obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
    #     ret = self.postRequest(obj)
    #     return ret
