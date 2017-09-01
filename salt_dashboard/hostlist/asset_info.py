# -*- coding: utf-8 -*-
from saltapi.saltAPI import saltAPI

import threading
asset_info = []

def get_server_asset_info(tgt):
    '''
    Salt API得到资产信息，进行格式化输出
    '''
    global asset_info
    info = []
    sapi = saltAPI()
    ret = sapi.SaltMinions(tgt)['return'][0][tgt]
    ip = ret['ipv4'][1]
    info.append(ip)
    hostname = ret['id']
    info.append(hostname)
    fqdn = ret['fqdn']
    info.append(fqdn)
    domain = ret['domain']
    info.append(domain)
    macaddress = ret['hwaddr_interfaces']['ens33']
    info.append(macaddress)
    os = ret['os']
    info.append(os)
    osarch = ret['osarch']
    info.append(osarch)
    osrelease = ret['osrelease']
    info.append(osrelease)
    manufacturer = ret['manufacturer']
    info.append(manufacturer)
    productname = ret['productname']
    info.append(productname)
    serialnumber = ret['serialnumber']
    info.append(serialnumber)
    cpu_model = ret['cpu_model']
    info.append(cpu_model)
    num_cpus = int(ret['num_cpus'])
    info.append(num_cpus)
    num_gpus = int(ret['num_gpus'])
    info.append(num_gpus)
    mem_total = str(ret['mem_total']) + 'MB'
    info.append(mem_total)
    virtual = ret['virtual']
    info.append(virtual)
    asset_info.append(info)


def multitle_collect(tgt):
    global asset_info
    #全局变量置空,避免多次请求的时候返回结果叠加
    aseet_info = []
    threads = []
    loop = 0
    numtgt = len(tgt)
    for i in range(0, numtgt, 2):
        nkeys = range(loop*2, (loop+1)*2, 1)
        #实例化线程
        for i in nkeys:
            if i >= numtgt:
                break
            else:
                t = threading.Thread(target=get_server_asset_info, args=(tgt[i],))
                threads.append(t)
        #启动线程
        for i in nkeys:
            if i >= numtgt:
                break
            else:
                threads[i].start()
        #等待并发线程结束
        for i in nkeys:
            if i >= numtgt:
                break
            else:
                threads[i].join()
        loop = loop + 1
    return asset_info