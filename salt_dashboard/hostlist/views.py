from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from hostlist import models
from saltapi.saltAPI import saltAPI
from hostlist.models import HostList, HostAsset, IdcAsset, Maintainer
from hostlist.asset_info import *
from django.contrib.auth.decorators import login_required
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import json

# Create your views here.
def idc_list(request):
    """
    list all idc
    """
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    idc_list = IdcAsset.objects.all()
    p = Paginator(idc_list, 7, request=request)
    idc_list = p.page(page)

    return render(request, 'idc_list.html', locals())

def host_list(request):
    '''
    list all host
    '''
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    all_host = HostList.objects.all()
    idc_list = IdcAsset.objects.all()
    user_list = Maintainer.objects.all()

    idc_id = request.GET.get('idc_id')
    user_id = request.GET.get('user_id')
    hostname = request.POST.get('hostname')
    if idc_id:
        all_host = HostList.objects.filter(idc = idc_id)
    elif user_id:
        all_host = HostList.objects.filter(maintainer = user_id)
    elif hostname:
        all_host = HostList.objects.filter(ip__hostname__icontains = hostname)
    else:
        all_host = all_host.order_by('ip')
    p = Paginator(all_host, 7, request=request)
    all_host = p.page(page)

    return render(request, 'host_list.html', locals())

def get_hostasset(request):
    """
    get all hostasset
    """
    if request.method == 'GET':
        action = request.get_full_path().split('=')[1]
        if action == 'refresh':
            sapi = saltAPI()
            accepted, denied, unaccept, rejected = sapi.list_all_key()
            tgt = [i for i in accepted]
            ret = multitle_collect(tgt)
            for i in ret:
                h = HostAsset.objects.get_or_create(ip=i[0], hostname=i[1], fqdn=i[2], domain=i[3], macaddress=i[4], os=i[5],osarch=i[6], osrelease=i[7], manufacturer=i[8], productname=i[9], serialnumber=i[10], cpu_model=i[11], cpu_nums=i[12], cpu_groups=i[13], mem=i[14], virtual=i[15])
                HostList.objects.get_or_create(ip = h[0])
        return HttpResponseRedirect(reverse('host_list'))

def hostasset_list(request, ip):
    """
    list all hostasset
    """
    all_hostasset = HostAsset.objects.get(ip = ip)
    return render(request, 'hostasset_list.html', locals())