import copy


@staticmethod
def schedule(managers, resources, alloc_req, constraints):
   '''   
   Managers: {'1d1c5582-1b74-11e5-bba3-60a44cabf185': {'Name': u'IRM-SEAL\n', 'ManagerID': '1d1c5582-1b74-11e5-bba3-60a44cabf185', 'Port': 54106, 'Address': '127.0.0.1'}, '1e2e967e-1b74-11e5-bba3-60a44cabf185': {'Name': u'IRM-HERON\n', 'ManagerID': '1e2e967e-1b74-11e5-bba3-60a44cabf185', 'Port': 51186, 'Address': '127.0.0.1'}}

   Resources: {'1d1c5582-1b74-11e5-bba3-60a44cabf185': {u'ID2': {u'Attributes': {u'a': 9, u'c': 5, u'b': 4}, u'Type': u'Device'}, u'ID3': {u'Attributes': {u'a': 2, u'c': 8, u'b': 10}, u'Type': u'Device'}, u'ID1': {u'Attributes': {u'a': 2, u'c': 5, u'b': 3}, u'Type': u'Device'}}, '1e2e967e-1b74-11e5-bba3-60a44cabf185': {u'ID2': {u'Attributes': {u'a': 4, u'c': 2, u'b': 8}, u'Type': u'Device'}, u'ID3': {u'Attributes': {u'a': 2, u'c': 7, u'b': 3}, u'Type': u'Device'}, u'ID1': {u'Attributes': {u'a': 2, u'c': 3, u'b': 5}, u'Type': u'Device'}}}

   Allocations: [{u'Group': u'g0', u'Type': u'Machine', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g0', u'Type': u'Machine', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g0', u'Type': u'DFECluster', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}]
   '''
   state_res = copy.copy(resources)
   print ":::>", state_res
   for rq in alloc_req:
      for rs in state_res:
         print ":::>", rs
      
      

   
