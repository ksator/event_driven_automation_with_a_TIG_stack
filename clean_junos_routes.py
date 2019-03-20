from jnpr.junos import Device
from jnpr.junos.utils.config import Config

def clean_routing_table():
    device=Device (host='100.123.1.3', user='jcluser', password='Juniper!1')
    device.open()
    cfg=Config(device, mode='private')
    cfg.load(path='junos_configuration/clean_routes.conf', format='text')
    cfg.commit()
    device.close()


clean_routing_table()

