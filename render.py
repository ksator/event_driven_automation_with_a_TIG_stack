from yaml import load
from jinja2 import Template

################ get the variables value ##############

my_variables_file=open('variables.yml', 'r')
my_variables_in_string=my_variables_file.read()
my_variables_in_yaml=load(my_variables_in_string)
my_variables_file.close()

################# render minion conf file ###################

f=open('templates/minion.j2')
my_template = Template(f.read())
f.close()

f=open('render/minion','w')
f.write(my_template.render(my_variables_in_yaml))
f.close()

################ render proxy config file ###################

f=open('templates/proxy.j2')
my_template = Template(f.read())
f.close()

f=open('render/proxy','w')
f.write(my_template.render(my_variables_in_yaml))
f.close()


################### render junos configuration file #################

f=open('templates/syslog.j2')
my_template = Template(f.read())
f.close()

f=open('render/salt/syslog.conf','w')
f.write(my_template.render(my_variables_in_yaml))
f.close()

################### render pillar files ################################
f=open('templates/pillars_top.j2')
my_template = Template(f.read())
f.close()

f=open('render/pillar/top.sls','w')
f.write(my_template.render(my_variables_in_yaml))
f.close()

f=open('templates/pillars_device.j2')
my_template = Template(f.read())
f.close()

for item in my_variables_in_yaml['junos']:
    f=open('render/pillar/' + item['name'] +'-details.sls','w')
    f.write(my_template.render(item))
    f.close()


