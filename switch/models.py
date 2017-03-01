from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Switch(models.Model):
    name=models.CharField(max_length=30)
    host=models.CharField(max_length=30)
    user=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    lookback=models.CharField(max_length=30)
    type=models.CharField(max_length=30)
    linkport=models.CharField(max_length=30)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

class tunnel(models.Model):
    tunelid=models.CharField(max_length=30)
    src=models.CharField(max_length=30)
    dst=models.CharField(max_length=30)
    host=models.CharField(max_length=30)

    def __str__(self):  # __unicode__ on Python 2
        return self.tunelid

class bill(models.Model):
    billid=models.CharField(max_length=30)
    customer=models.CharField(max_length=30)
    subnet_vni=models.IntegerField()
    P1=models.CharField(max_length=30)
    P2=models.CharField(max_length=30)
    def __str__(self):  # __unicode__ on Python 2
        return self.billid

class customer(models.Model):
    customer=models.CharField(max_length=30)
    P=models.CharField(max_length=30)
    customerVlan=models.CharField(max_length=30)
    def __str__(self):  # __unicode__ on Python 2
        return self.customer

class vxlan(models.Model):
    host=models.CharField(max_length=30)
    vsi=models.CharField(max_length=30)
    vxlanid=models.CharField(max_length=30)
    tunnelid=models.CharField(max_length=30)
    billid=models.CharField(max_length=30)
    def __str__(self):  # __unicode__ on Python 2
        return self.vsi

class L2Ethservice(models.Model):
    host=models.CharField(max_length=30)
    port=models.CharField(max_length=30)
    vsi=models.CharField(max_length=30)
    instance=models.CharField(max_length=30)
    vlanid=models.CharField(max_length=30)
    vxlanid=models.CharField(max_length=30)
    billid=models.CharField(max_length=30)
    def __str__(self):  # __unicode__ on Python 2
        return self.instance