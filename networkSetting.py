# -*- coding: utf-8 -*-
import os
from time import sleep
from wmi import WMI


def getAdapter():
    global colNicConfigs
    wmiService = WMI()
    #获取到本地有网卡信息
    colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
    i = 0
    for obj in colNicConfigs:
        print(obj.Description)
        i = i + 1
    return i

def runSet(index):
    adapter = colNicConfigs[index]
    ip = input("请输入ip地址（如：10.10.39.129）")
    SubnetMasks = input("请输入子网掩码（如：255.255.255.0）")
    DefaultGateways = input("请输入网关（如：10.10.39.254）")
    DNSServers = input("请输入DNS（默认为：114.114.114.114）")
    GatewayCostMetrics = input("请输入地址获取方式（1为非自动。0为自动）")
    arrGatewayCostMetrics = [GatewayCostMetrics]
    if DNSServers == "":
        DNSServers = "114.114.114.114"
    arrIP = [ip]
    arrSubnetMasks = [SubnetMasks]
    arrDefaultGateways = [DefaultGateways]
    arrDNS = [DNSServers]
    ipRes = adapter.EnableStatic(IPAddress=arrIP, SubnetMask=arrSubnetMasks)
    if ipRes[0] == 0:
        print
        u'\ttip:设置IP成功'
        print
        u'\t当前ip：%s' % ip
    else:
        if ipRes[0] == 1:
            print
            u'\ttip:设置IP成功，需要重启计算机！'
        else:
            print
            u'\ttip:修改IP失败: IP设置发生错误'
            return False
    # 开始执行修改dns
    wayRes = adapter.SetGateways(DefaultIPGateway=arrDefaultGateways, GatewayCostMetric=arrGatewayCostMetrics)
    if wayRes[0] == 0:
        print
        u'\ttip:设置网关成功'
    else:
        print
        u'\ttip:修改网关失败: 网关设置发生错误'
        return False
    dnsRes = adapter.SetDNSServerSearchOrder(DNSServerSearchOrder=arrDNS)
    if dnsRes[0] == 0:
        print
        u'\ttip:设置DNS成功,等待3秒刷新缓存'
        sleep(3)
        os.system('ipconfig /flushdns')
    else:
        print
        u'\ttip:修改DNS失败: DNS设置发生错误'
        return False
if __name__ == '__main__':
    i = str(getAdapter())
    index = eval(input("请选择网卡(1-" +i+")"))
    runSet(index-1)
