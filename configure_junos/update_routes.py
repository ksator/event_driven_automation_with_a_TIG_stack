from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jinja2 import Template
from time import time, sleep

def update_junos():
    device=Device (host='100.123.1.3', user='jcluser', password='Juniper!1')
    device.open()
    cfg=Config(device, mode='private')
    cfg.load(path='configure_junos/update_routes.conf', format='text')
    cfg.commit()
    device.close()


update_junos()

