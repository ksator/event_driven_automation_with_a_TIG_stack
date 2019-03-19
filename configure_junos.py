from jinja2 import Template
from yaml import load
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

# template to configure junos
f=open('configure_junos/junos.j2')
my_template = Template(f.read())
f.close()

# get devices list. each item has an ip, name, username, password.
f=open('variables.yml', 'r')
devices_list = load(f.read())['junos']
f.close()

# get junos variables: interfaces, asn, ....
f=open('configure_junos/junos.yml', 'r')
junos_vars = load(f.read())
f.close()

for item in devices_list:
    device=Device (host=item['ip'], user=item['username'], password=item['passwd'])
    host_vars = junos_vars[item['name']]
    f=open('configure_junos/' + item['name'] + '.conf','w')
    f.write(my_template.render(host_vars))
    f.close()
    junos_conf = 'configure_junos/' + item['name'] + '.conf'
    device.open()
    cfg=Config(device)
    cfg.load(path=junos_conf, format='text')
    cfg.commit()
    device.close()
    print 'configured device ' + item['name']


