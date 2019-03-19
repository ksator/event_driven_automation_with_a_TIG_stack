from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jinja2 import Template
from time import time, sleep

def clean_routing_table():
    device=Device (host='100.123.1.0', user='jcluser', password='Juniper!1')
    device.open()
    cfg=Config(device, mode='private')
    cfg.load(path='configure_junos/clean_routes.conf', format='text')
    cfg.commit()
    device.close()


clean_routing_table()

