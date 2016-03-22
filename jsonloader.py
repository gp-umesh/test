import os
import json

f = open('/home/grampower/00:04:00.json').read()
data = json.loads(f)
for i in range (len(data['snapshot_list'][0].values()[1])):

#print data['grid_name']
   node_list = data['snapshot_list'][0].values()[1]
#print node_list
   print node_list[i]['address'] + "     "+ str(node_list[i]['voltage'])                      
#print data

#print js

