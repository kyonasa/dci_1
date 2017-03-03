from django.shortcuts import render
from .models import Switch,tunnel,bill,customer,vxlan,L2Ethservice
from pyhp.comware import HPCOM7
from pyhp.features.ping import Ping
from pyhp.features.vxlan import Tunnel,Vxlan
from pyhp.features.vxlan import L2EthService as l2es

# Create your views here.
# coding:utf-8
from django.http import HttpResponse


def ctunnel(request):
    host='host3'
    args1 = dict(host=Switch.objects.filter(name=host)[0].host,
                 username=Switch.objects.filter(name=host)[0].user,
                 password=Switch.objects.filter(name=host)[0].password,
                 port=830)
    device1=HPCOM7(**args1)
    device1.open()
    tunnelid='5'
    # ping1=Ping(device1,'10.3.214.22')
    tunnel1=Tunnel(device1,tunnelid)
    tunnel.objects.get_or_create(tunelid=tunnelid,
                                 src=tunnel1.get_config()['src'],
                                 dst=tunnel1.get_config()['dest'],
                                 host=Switch.objects.filter(name=host)[0].host)
    return HttpResponse(str(tunnel1.get_config()['dest']))

def billDepand(request):
    billid='4'
    result='result:'
    try:
        Bill=bill.objects.get(billid=billid)
    except:
        result=result,';','bill not found'
    try:
        switch1=Switch.objects.get(name=bill.objects.get(billid=billid).P1)
    except:
        result=result,';','P1 not found'
    try:
        switch2=Switch.objects.get(name=bill.objects.get(billid=billid).P2)
    except:
        result=result,';','P2 not found'
    try:
        if switch1.type=='h3c':
            tunnel1=tunnel.objects.get(host=switch1.host,src=switch1.lookback,dst=switch2.lookback)
            customer1 = customer.objects.get(customer=Bill.customer,
                                         P=Bill.P1)
            vxlan.objects.get_or_create(host=switch1.host,
                                        vsi=str(customer1.customer)+str(Bill.subnet_vni),
                                        vxlanid=Bill.subnet_vni,
                                        tunnelid=tunnel1.tunelid,
                                        billid=billid)
            L2Ethservice.objects.get_or_create(host=switch1.host,
                                               vsi=str(customer1.customer)+str(Bill.subnet_vni),
                                               port=switch1.linkport,
                                               instance=str(customer1.customerVlan),
                                               vlanid=customer1.customerVlan,
                                               vxlanid=Bill.subnet_vni,
                                               billid=billid)
            result=result,';','switch1s configuration is ok'

        else:
            result=result,';','switch 1 type not support yet'
    except:
        result=result,';','switch1 not avaliable'
    try:
        if switch2.type=='h3c':
            tunnel2=tunnel.objects.get(host=switch2.host,src=switch2.lookback,dst=switch1.lookback)
            customer2=customer.objects.get(customer=Bill.customer,
                                       P=Bill.P2)
            vxlan.objects.get_or_create(host=switch2.host,
                                        vsi=str(customer2.customer)+str(Bill.subnet_vni),
                                        vxlanid=Bill.subnet_vni,
                                        tunnelid=tunnel2.tunelid,
                                        billid=billid)
            L2Ethservice.objects.get_or_create(host=switch2.host,
                                               vsi=str(customer2.customer)+str(Bill.subnet_vni),
                                               port=switch2.linkport,
                                               instance=str(customer2.customerVlan),
                                               vlanid=customer2.customerVlan,
                                               vxlanid=Bill.subnet_vni,
                                               billid=billid)
            result=result,';','switch2s configuration is ok'
        else:
            result = result,';','switch 2 type not support yet'
    except:
        result=result,';','switch2 not available'
    return HttpResponse(result)

def cfg(request):
    try:
        billid = '4'
        result = 'result:'
        try:
            Bill = bill.objects.get(billid=billid)
        except:
            result = result, ';', 'bill not found'
        try:
            switch2 = Switch.objects.get(name=Bill.P2)
            if switch2.type=='h3c':
                args2 = dict(host=switch2.host,
                             username=switch2.user,
                             password=switch2.password,
                             port=830)
                device2=HPCOM7(**args2)
                device2.open()
                vxlan2=Vxlan(device2,
                             str(Bill.subnet_vni),
                             vsi=vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).vsi)
                l2es2=l2es(device2,
                           L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).port,
                           str(L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).instance),
                           str(vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).vsi))

                vxlan2.create()
                vxlan2.build(tunnels_to_add=[str(vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).tunnelid)])
                device2.execute()
                print (l2es2.get_config())
                print (l2es2.build(vsi=str(vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).vsi),
                            instance=str(L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).instance),
                            encap='s-vid',
                            vlanid=str(L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).vlanid),
                            access_mode='vlan'))

                device2.execute()
                print (vxlan2.get_config())
                print (l2es2.get_config())
                result=result,'P2 sucessful'
            else:
                result=result,';','switch 1 type not support yet'
        except:
            result = result, ';', 'P2 not found'
        try:
            switch1 = Switch.objects.get(name=Bill.P1)
            if switch1.type=='h3c':
                args1 = dict(host=switch1.host,
                             username=switch1.user,
                             password=switch1.password,
                             port=830)
                device1=HPCOM7(**args1)
                device1.open()
                vxlan1=Vxlan(device1,
                             str(Bill.subnet_vni),
                             vsi=vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch1.host,billid=billid).vsi)
                l2es1=l2es(device1,
                           L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch1.host,billid=billid).port,
                           str(L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch1.host,billid=billid).instance),
                           str(vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch1.host,billid=billid).vsi))

                vxlan1.create()
                vxlan1.build(tunnels_to_add=[str(vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch1.host,billid=billid).tunnelid)])
                device1.execute()
                print (l2es1.get_config())
                print (l2es1.build(vsi=str(vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch1.host,billid=billid).vsi),
                            instance=str(L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch1.host,billid=billid).instance),
                            encap='s-vid',
                            vlanid=str(L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch1.host,billid=billid).vlanid),
                            access_mode='vlan'))

                device1.execute()
                print (vxlan1.get_config())
                print (l2es1.get_config())
                result=result,'P1 sucessful'
            else:
                result=result,';','switch 1 type not support yet'
        except:
            result = result, ';', 'P1 not found'
    except:
        result=result,'cfg failed'
    return HttpResponse(result)

def deleteB(request):
    try:
        billid = '3'
        result = 'result:'
        try:
            Bill = bill.objects.get(billid=billid)
        except:
            result = result, ';', 'bill not found'
        try:
            switch2 = Switch.objects.get(name=Bill.P2)
            if switch2.type=='h3c':
                args2 = dict(host=switch2.host,
                             username=switch2.user,
                             password=switch2.password,
                             port=830)
                device2=HPCOM7(**args2)
                device2.open()
                vxlan2=Vxlan(device2,
                             str(Bill.subnet_vni),
                             vsi=vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).vsi)
                l2es2=l2es(device2,
                           L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).port,
                           str(L2Ethservice.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).instance),
                           str(vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).vsi))
                try:
                    vxlan2.remove_vxlan()
                    vxlan2.remove_vsi(vsi=vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).vsi)
                    l2es2.remove()
                    device2.execute()
                    result=result,'P2 deleted'
                except:
                    result=result,'vxlan already deleted'
            else:
                result = result, ';', 'switch 2 type not support yet'
        except:
            result = result, ';', 'P2 not found'
        try:
            switch1 = Switch.objects.get(name=Bill.P1)
            if switch1.type == 'h3c':
                args1 = dict(host=switch1.host,
                             username=switch1.user,
                             password=switch1.password,
                             port=830)
                device1 = HPCOM7(**args1)
                device1.open()
                vxlan1 = Vxlan(device1,
                               str(Bill.subnet_vni),
                               vsi=vxlan.objects.get(vxlanid=Bill.subnet_vni, host=switch1.host, billid=billid).vsi)
                l2es1 = l2es(device1,
                             L2Ethservice.objects.get(vxlanid=Bill.subnet_vni, host=switch1.host, billid=billid).port,
                             str(L2Ethservice.objects.get(vxlanid=Bill.subnet_vni, host=switch1.host,
                                                          billid=billid).instance),
                             str(vxlan.objects.get(vxlanid=Bill.subnet_vni, host=switch1.host, billid=billid).vsi))
                try:
                    vxlan1.remove_vxlan()
                    vxlan1.remove_vsi(vsi=vxlan.objects.get(vxlanid=Bill.subnet_vni,host=switch2.host,billid=billid).vsi)
                    l2es1.remove()
                    device1.execute()
                    result=result,'P1 deleted'
                except:
                    result = result, 'vxlan already deleted'
            else:
                result = result, ';', 'switch 1 type not support yet'
        except:
            result = result, ';', 'P1 not found'
    except:
        result=result,';','bill deleted faided'
    return HttpResponse(result)