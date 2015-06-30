import deps
import copy
from hresman import utils

def compute_capacity(managers, mgr_id, resource, request):

   if mgr_id not in managers:
      raise Exception("cannot find manager: " + mgr_id)
   
   addr = managers[mgr_id]['Address']
   port = managers[mgr_id]['Port']
   
   data = {'Resource': resource, "Allocation": [{"Attributes": request["Attributes"]}], "Release": []}
   ret= utils.post(data, 'v3/resources/calc-capacity', port, addr)
   if "result" not in ret:
      raise Exception("cannot calculate capacity!")

   return ret["result"]

def match_constraints(constraints, resID, resource, alloc):

    match = True       
    for constraint in constraints:
        if ("Source" in constraint) and \
           ("ConstraintType" in constraint) and ("Group" in alloc):
          if ("ID" in constraint) and (constraint["Source"] == alloc["Group"]):
             eval_str = "'" + str(constraint["ID"]) + "' " + constraint["ConstraintType"] + " '" + str(resID) + "'"
             if not (eval(eval_str)):
                match = False
                break  
        else:
           raise Exception("malformed constraint: " + str(constraint))         
    return match      

@staticmethod
def schedule(managers, resources, alloc_req, constraints):
   '''   
   Managers: {'1d1c5582-1b74-11e5-bba3-60a44cabf185': {'Name': u'IRM-SEAL\n', 'ManagerID': '1d1c5582-1b74-11e5-bba3-60a44cabf185', 'Port': 54106, 'Address': '127.0.0.1'}, '1e2e967e-1b74-11e5-bba3-60a44cabf185': {'Name': u'IRM-HERON\n', 'ManagerID': '1e2e967e-1b74-11e5-bba3-60a44cabf185', 'Port': 51186, 'Address': '127.0.0.1'}}

   Resources: {'1d1c5582-1b74-11e5-bba3-60a44cabf185': {u'ID2': {u'Attributes': {u'a': 9, u'c': 5, u'b': 4}, u'Type': u'Device'}, u'ID3': {u'Attributes': {u'a': 2, u'c': 8, u'b': 10}, u'Type': u'Device'}, u'ID1': {u'Attributes': {u'a': 2, u'c': 5, u'b': 3}, u'Type': u'Device'}}, '1e2e967e-1b74-11e5-bba3-60a44cabf185': {u'ID2': {u'Attributes': {u'a': 4, u'c': 2, u'b': 8}, u'Type': u'Device'}, u'ID3': {u'Attributes': {u'a': 2, u'c': 7, u'b': 3}, u'Type': u'Device'}, u'ID1': {u'Attributes': {u'a': 2, u'c': 3, u'b': 5}, u'Type': u'Device'}}}

   Allocations: [{u'Group': u'g0', u'Type': u'Machine', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g0', u'Type': u'Machine', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g0', u'Type': u'DFECluster', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}]
   '''
   state_res = copy.deepcopy(resources)
   result = []
   for rq in alloc_req:
      sc = {}
      for mgr in state_res:
         resources = state_res[mgr]
         for res in resources:
            if resources[res]['Type'] == rq['Type'] and match_constraints(constraints, res, resources, rq):
               ret = compute_capacity(managers, mgr, resources[res], rq)
               if ret != {}:
                  resources[res]["Attributes"] = ret["Resource"]["Attributes"]
                  sc = {"manager": mgr, "res_id": res, "alloc_req": rq}
                  break 
         if sc != {}:
            break
      if sc == {}:
         raise Exception("cannot find a schedule!")
      result.append(sc)
   return result

               
         
         
               
      
      

   
