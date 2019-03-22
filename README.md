This repository is about **Event driven automation with a TIG stack and SaltStack**.   

Visit [**wiki**](https://github.com/ksator/event_driven_automation_with_a_TIG_stack/wiki) for instructions  

Lab topology
![topology.png](https://github.com/ksator/event_driven_automation_with_a_TIG_stack/blob/master/resources/topology.png)  

BGP (data pulled with SNMP)
![BGP.png](https://github.com/ksator/event_driven_automation_with_a_TIG_stack/blob/master/resources/BGP.png)  

BGP (data pushed with Openconfig)
![EBGP_sessions_Openconfig.png](https://github.com/ksator/event_driven_automation_with_a_TIG_stack/blob/master/resources/EBGP_sessions_Openconfig.png)  

Grafana is configured to send a webhook notification (HTTP POST with a JSON body) to SaltStack when one of the spine has less than 4 BGP sessions established.  
SaltStack is configured to manage automatically tickets on Request Tracker.   

The BGP session between the spine vMX1 and the leaf vMX5 is not anymore established.   
 
SaltStack created a ticket on Request Tracker, and updated the ticket with some details.     

