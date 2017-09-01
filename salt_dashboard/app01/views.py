from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from app01 import models
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from saltapi.saltAPI import saltAPI
from app01.models import Module, Command, Minions, Result
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json
import re
# Create your views here.

#key列表 key接受 key删除
def minions_collect(minion, status='Unknown'):
    try:
        sapi = saltAPI()
        Minions.objects.get_or_create(minion=minion)
        Minion=Minions.objects.get(minion=minion)

        if status=='Accepted':
            grains=sapi.SaltMinions(minion)['return'][0][minion]
            pillar=sapi.SaltCmd(tgt=minion,fun='pillar.items',client='local')['return'][0][minion]
            Minion.grains=json.dumps(grains)
            Minion.pillar=json.dumps(pillar)
        Minion.status=status
        Minion.save()
        result=True
    except Exception as e:
        result=str(e)
    return result

def salt_key_list(request):
    context = {}
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    try:
        sapi = saltAPI()
        #对所有key刷新minions表数据
        a,d,u,r=sapi.list_all_key()
        if a:
            for m in a:
                minions_collect(m,'Accepted')
        if d:
            for m in d:
                minions_collect(m,'Denied')
        if u:
            for m in u:
                minions_collect(m,'Unaccepted')
        if r:
            for m in r:
                minions_collect(m,'Rejected')
        #minion不存在对应的key时设为未知
        keys=[]
        for s in [a,d,u,r]:
            for m in s:
                keys.append(m)
        minion_list=Minions.objects.all()
        ms=[]
        for m in minion_list:
            if m.minion not in keys:
                m.status='Unknown'
                m.save()
            grains=json.loads(m.grains)
            ip=grains['ipv4'][1]
            obj={'id':m.id,'minion':m.minion,'ip':ip,'os':grains['os'],'status':m.status}
            ms.append(obj)

        p = Paginator(ms, 7, request=request)
        ms = p.page(page)

        context['minion_list']=ms
    except Exception as error:
        context['error']=error
        # print error
    return render(request,'salt_key_list.html',context)

def salt_key_fun(request):
    id=request.GET.get('id','')
    active=request.GET.get('active','')
    if request.is_ajax() and id and active:
        try:
            minion=Minions.objects.get(id=id)
            sapi = saltAPI()
            if id:
                if active == 'delete':
                    success=sapi.delete_key(minion)
                    if success:
                        minion.status='Unknown'
                        minion.save()
                        result=u'KEY"%s"删除成功！'%minion.minion
                    else:
                        result=u'KEY"%s"删除失败！'%minion.minion
                elif active == 'accept':
                    success=sapi.accept_key(minion)
                    if success:
                        minions_collect(minion.minion,'Accepted')
                        result=u'KEY"%s"接受成功！'%minion.minion
                    else:
                        result=u'KEY"%s"接受失败！'%minion.minion
                elif active == 'grains':
                    result=json.loads(minion.grains)
                elif active == 'pillar':
                    result=json.loads(minion.pillar)
        except Exception as e:
            result=str(e)
        return JsonResponse(result,safe=False)

# def salt_key_list(request):
#     """
#     list all key
#     """
#     sapi = saltAPI()
#     minions,minions_pre = sapi.list_all_key()

#     # try:
#     #     sapi = saltAPI()
#     #     result=sapi.SaltRun(client='runner',fun='manage.status')
#     #     context['minions_up']=result['return'][0]['up']
#     #     context['minions_down']=result['return'][0]['down']
#     # except Exception as error:
#     #     context['error']=error

#     return render(request, 'salt_key_list.html', {'all_minions': minions, 'all_minions_pre': minions_pre})

# def salt_accept_key(request):
#     """
#     accept salt minions key
#     """
#     node_name = request.GET.get('node_name')
#     sapi = saltAPI()
#     ret = sapi.accept_key(node_name)
#     Message.objects.create(type='salt', action='key', action_ip=node_name, content='saltstack accept node key')
#     return HttpResponseRedirect(reverse('salt:key_list'))

# def salt_delete_key(request):
#     """
#     delete salt minions key
#     """
#     node_name = request.GET.get('node_name')
#     sapi = saltAPI()
#     ret = sapi.delete_key(node_name)
#     Message.objects.create(type='salt', action='key', action_ip=node_name, content='saltstack delete node key')
#     return HttpResponseRedirect(reverse('salt:key_list'))

#命令列表
def command(request):
    module_id = request.GET.get('module_id')
    module_name = request.GET.get('module_name')
    client = request.GET.get('client')
    cmd = request.GET.get('cmd')
    active = request.GET.get('active')
    context={}

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    #命令收集
    if active=='collect':
        try:
            sapi = saltAPI()
            funs=['doc.runner','doc.wheel','doc.execution']
            for fun in funs:
                result = sapi.SaltRun(fun=fun,client='runner')
                cs=result['return'][0]
                for c in cs:
                    Module.objects.get_or_create(client=fun.split('.')[1],name=c.split('.')[0])
                    module=Module.objects.get(client=fun.split('.')[1],name=c.split('.')[0])
                    Command.objects.get_or_create(cmd=c,module=module)
                    command=Command.objects.get(cmd=c,module=module)
                    if not command.doc:
                        command.doc=cs[c]
                        command.save()
            context['success']=u'命令收集完成！'
        except Exception as error:
            context['error']=error

    cmd_list=Command.objects.order_by('cmd')
    module_list=Module.objects.order_by('client','name')
    #按模块过滤
    if request.method=='GET' and module_id:
            cmd_list = cmd_list.filter(module=module_id)

    if request.is_ajax() and client:
        if re.search('runner',client):
            client='runner'
        elif re.search('wheel',client):
            client='wheel'
        else:
            client='execution'
    #命令帮助信息
        if cmd:
            try:
                command=Command.objects.get(cmd=cmd,module__client=client)
                doc=command.doc.replace("\n","<br>").replace(" ","&nbsp;")
            except Exception as error:
                doc=str(error)
            return JsonResponse(doc,safe=False)
    #请求模块下的命令
        elif module_name:
            cmd_list = cmd_list.filter(module__client=client,module__name=module_name).order_by('-cmd')
            cmd_list = [cmd.cmd for cmd in cmd_list]
            return JsonResponse(cmd_list,safe=False)
    #请求CLIENT下的模块
        else:
            module_list=module_list.filter(client=client)
            module_list=[module.name for module in module_list.order_by('-name')]
            return JsonResponse(module_list,safe=False)

    p = Paginator(cmd_list, 7, request=request)
    cmd_list = p.page(page)

    context['cmd_list']=cmd_list
    context['module_list']=module_list

    return render(request, 'salt_command.html', context)

#命令执行
def execute(request):
    module_list=Module.objects.filter(client='execution').order_by('name')
    minion_list=Minions.objects.filter(status='Accepted')
    context={'module_list':module_list,'minion_list':minion_list}
    return render(request,'salt_execute.html',context)

def execute_fun(request):
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id')
        client = request.GET.get('client')
        tgt_type = request.GET.get('tgt_type')
        tgt  = request.GET.get('tgt','')
        fun = request.GET.get('fun')
        arg = request.GET.get('arg','')
        user  = request.user.username
        if id:
            r = Result.objects.get(id=id)
            result = json.loads(r.result) #result.html默认从数据库中读取
        else:
            try:
                sapi = saltAPI()
                if re.search('runner',client) or re.search('wheel',client):
                    r = sapi.SaltRun(client=client,fun=fun,arg=arg)
                else:
                    r = sapi.SaltCmd(client=client,tgt=tgt,fun=fun,arg=arg,expr_form=tgt_type)
                if re.search('async',client):
                    jid = r['return'][0]['jid']
                    result = jid #异步命令只返回JID，之后JS会调用jid_info
                    # minions = ','.join(result['return'][0]['minions'])
                    Res=Result(client=client,jid=jid,minions=tgt,fun=fun,arg=arg,tgt_type=tgt_type,user=user)
                    Res.save()
                else:
                    result=r['return'][0]#同步命令直接返回结果
                    Res=Result(client=client,minions=tgt,fun=fun,arg=arg,tgt_type=tgt_type,user=user,result=json.dumps(result))
                    Res.save()
                # res=model_to_dict(r,exclude='result')
            except Exception as e:
                result={'Error': str(e)}

        return JsonResponse(result,safe=False)
#执行结果
def result(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    result_list = Result.objects.order_by('-id')
    p = Paginator(result_list, 7, request=request)
    result_list = p.page(page)
    return render(request, 'result.html', locals())

#任务信息
def jid_info(request):
    jid = request.GET.get('jid')
    if jid:
        try:
            r = Result.objects.get(jid=jid)
            if r.result and r.result!='{}' :
                result = json.loads(r.result) #cmd_result.html默认从数据库中读取
            else:
                sapi = saltAPI()
                jid_in = sapi.SaltJob(jid)
                result = jid_in['info'][0]['Result']
                r.result = json.dumps(result)
                r.save()
        except Exception as e:
            result={'error':str(e)}
        return JsonResponse(result,safe=False)
