from yaml import load
from jnpr.junos.utils.sw import SW
from jnpr.junos import Device

f=open('variables.yml', 'r')
devices_list = load(f.read())['junos']
f.close()

pkgs_list = ['network-agent-x86-32-18.2R1-S3.2-C1.tgz', 'junos-openconfig-x86-32-0.0.0.10-1.tgz']

for pkg in pkgs_list:
    for item in devices_list:
        print 'adding the package ' + pkg + ' to the device ' + item['name']
        device=Device (host=item['ip'], user=item['username'], password=item['passwd'])
        device.open()
        sw = SW(device)
        sw.install(package=pkg, validate=False, no_copy=False, progress=True, remote_path="/var/home/jcluser")
        device.close()


