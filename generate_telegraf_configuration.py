from yaml import load
from jinja2 import Template

################ get the variables value ##############

my_variables_file=open('variables.yml', 'r')
my_variables_in_string=my_variables_file.read()
my_variables_in_yaml=load(my_variables_in_string)
my_variables_file.close()

################# render telegraf openconfig configuration file ###################

f=open('tig_configuration/telegraf-openconfig.j2')
my_template = Template(f.read())
f.close()

f=open('tig_configuration/telegraf-openconfig.conf','w')
f.write(my_template.render(my_variables_in_yaml))
f.close()

################# render telegraf snmp configuration file ###################

f=open('tig_configuration/telegraf-snmp.j2')
my_template = Template(f.read())
f.close()

f=open('tig_configuration/telegraf-snmp.conf','w')
f.write(my_template.render(my_variables_in_yaml))
f.close()

