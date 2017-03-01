from django.contrib import admin

# Register your models here.
from switch.models import Switch,tunnel,bill,customer,vxlan,L2Ethservice

class host(admin.ModelAdmin):
    list_display = ('host','name','user','password','lookback','linkport','type')

class tunnelAdmin(admin.ModelAdmin):
    list_display = ('tunelid','src','dst','host')

class billAdmin(admin.ModelAdmin):
    list_display = ('billid','customer','subnet_vni','P1','P2')

class customerAdmin(admin.ModelAdmin):
    list_display = ('customer','P','customerVlan')

class vxlanAdmin(admin.ModelAdmin):
    list_display = ('billid','host','vsi','vxlanid','tunnelid')

class L2EthserviceAdmin(admin.ModelAdmin):
    list_display = ('billid','host','vsi','port','instance','vlanid','vxlanid')

admin.site.register(Switch,host)
admin.site.register(tunnel,tunnelAdmin)
admin.site.register(bill,billAdmin)
admin.site.register(customer,customerAdmin)
admin.site.register(vxlan,vxlanAdmin)
admin.site.register(L2Ethservice,L2EthserviceAdmin)