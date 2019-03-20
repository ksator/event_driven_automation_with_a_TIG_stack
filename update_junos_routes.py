from jnpr.junos import Device
from jnpr.junos.utils.config import Config

def update_junos():
    device=Device (host='100.123.1.3', user='jcluser', password='Juniper!1')
    device.open()
    cfg=Config(device, mode='private')
    cfg.load(path='junos_configuration/update_routes.conf', format='text')
    cfg.commit()
    device.close()


update_junos()

