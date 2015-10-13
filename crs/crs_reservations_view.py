#!/usr/bin/env python

import deps

from flask.ext.classy import FlaskView, route
from flask import request

import hresman.utils

from hresman.utils import json_request, json_reply, json_error
from hresman.reservations_view import ReservationsView
from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView
import uuid
import json
import copy

class CRSReservationsView(ReservationsView):
    _scheduler=None
    
    @staticmethod
    def _select_scheduler(scheduler):
       if scheduler == "simple":
          import simple_scheduler
          CRSReservationsView._scheduler=simple_scheduler.schedule
       elif scheduler == "NC":
          import schedulerNC
          CRSReservationsView._scheduler=schedulerNC.schedule
       else:
          raise Exception("invalid scheduler: %s" % scheduler)

    
    ################################################################################
    '''
    [
    {
        "manager": "b542620e-3e7c-11e5-8686-60a44cabf185",
        "alloc_req": {
            "Group": "G1",
            "Type": "Machine",
            "Attributes": {
                "Cores": 1,
                "Subnet": "Gabriel",
                "Memory": 1024
            }
        },
        "res_id": "vagrant-ubuntu-trusty-64"
    },
    {
        "manager": "b542620e-3e7c-11e5-8686-60a44cabf185",
        "alloc_req": {
            "Group": "G2",
            "Type": "Machine",
            "Attributes": {
                "Cores": 1,
                "Subnet": "Gabriel",
                "Memory": 1024
            }
        },
        "res_id": "vagrant-ubuntu-trusty-64"
    },
    {
        "manager": "b542620e-3e7c-11e5-8686-60a44cabf185",
        "alloc_req": {
            "Attributes": {
                "AddressRange": "192.162.0.0/24",
                "Name": "Gabriel"
            },
            "Type": "Subnet"
        },
        "res_id": "ID-S0"
    },
    {
        "manager": "b542620e-3e7c-11e5-8686-60a44cabf185",
        "alloc_req": {
            "Attributes": {
                "IP": "10.1.0.107",
                "VM": "G2"
            },
            "Type": "PublicIP"
        },
        "res_id": "ID-P0"
    }
]
    ''' 
    def group_requests(self, sched):
       #print json.dumps(sched, indent=4)
       result = {}
       csched = copy.deepcopy(sched)
       rank = 0
       for req in csched:
          alloc = req["alloc_req"]
          alloc['ID'] = req['res_id']
          alloc['Rank'] = rank
          rank = rank + 1
          if req["manager"] not in result:
             result[req["manager"]] = []
          data = result[req["manager"]]   
          data.append(alloc)
       return result 
    
    ###############################################  create reservation ############ 
    def _create_reservation(self, scheduler, alloc_req, alloc_constraints, monitor):
        
       if scheduler != "":
          CRSReservationsView._select_scheduler(scheduler)
       
       
       schedule = self.group_requests(CRSReservationsView._scheduler(CRSManagersView.managers,\
                                      CRSResourcesView.resources, \
                                      alloc_req, alloc_constraints, CRSResourcesView.resource_constraints))
       
       #print json.dumps(schedule, indent=4)                                                                               
       iResIDs = []
       rollback = False
       for s in schedule:          
          addr = CRSManagersView.managers[s]['Address']
          port = CRSManagersView.managers[s]['Port']
          types = set(map(lambda x: x['Type'], schedule[s]))
   
          monitor_data = {}
          for m in monitor:
             if m in types:
                monitor_data[m] = monitor[m]
                
          if "PollTime" in monitor:
             monitor_data["PollTime"] = monitor["PollTime"]
                
          data = { "Allocation" : map(lambda x: { "Attributes": x["Attributes"], "Type": x["Type"], "ID": x["ID"]}, schedule[s]), 
                   "Monitor": monitor_data }

          try:
             ret = hresman.utils.post(data, 'createReservation', port, addr)

          except Exception as e:
             print "rolling back! " + str(e)
             rollback = True
          
          if (not rollback) and "result" not in ret:
             rollback = True
          
          if rollback:
             break
          else:
             # XtreemFS fix
             rID = map(lambda x: x if x.partition("/")[2] == "" else x.partition("/")[2], ret["result"]["ReservationID"])
             iResIDs.append({"addr": addr, "port": port, "name": CRSManagersView.managers[s]['Name'], \
                             "iRes": rID, "sched": schedule[s]})
       
       if not rollback:
          resID = uuid.uuid1()
          ReservationsView.reservations[str(resID)] = iResIDs
          print json.dumps(ReservationsView.reservations[str(resID)], indent=4)
       else:
          for iResID in iResIDs:
             data = {"ReservationID": iResID["iRes"]}
             try:                
                hresman.utils.delete_(data, 'releaseReservation', iResID["port"], iResID["addr"])
             except:
                pass  
          raise Exception("cannot make reservation! (rollbacking)")  
         
       return { "ReservationID" : [str(resID)] }                    
    
    ###############################################  check reservation ############   
    def _check_reservation(self, reservations):
       check_result = { "Instances": {} }
 
       for reservation in reservations:
          if reservation not in ReservationsView.reservations: 
             raise Exception("cannot find reservation: " + reservation)
          
          data = ReservationsView.reservations[reservation]
          ready = True
          ranked_addrs = []
          for alloc in data:
             ret = hresman.utils.post( { "ReservationID" : alloc["iRes"] }, "checkReservation", alloc["port"], alloc["addr"])
             if "result" not in ret:
                raise Exception("Error in checking reservation: ", str(ret))
             
             ranked_res = {k:v for (k,v) in map(lambda x,y: (y,x["Rank"]), alloc["sched"], alloc["iRes"])}    
                 
             instances = ret["result"]["Instances"]
             
             for i in instances:                
                ranked_addrs.append((ranked_res[i],instances[i]["Address"])) 
                status = instances[i]["Ready"]
                if type(status) is bool:
                   status = "TRUE"
                ready = ready and status.upper() == "TRUE"
          if ready:
             ranked_addrs.sort()
             addrs = []
             for r in ranked_addrs:
                addrs.extend(r[1]) 
             check_result["Instances"][reservation] = { "Ready": "True", "Address": addrs }
          else:
             check_result["Instances"][reservation] = { "Ready": "False" }      
       return check_result
       
       
    def _check_reservation_grouped(self, reservations):
       check_result = { "Instances": {} }
 
       for reservation in reservations:
          if reservation not in ReservationsView.reservations: 
             raise Exception("cannot find reservation: " + reservation)
          
          data = ReservationsView.reservations[reservation]
          ready = True
          addrs = []
          for alloc in data:
             ret = hresman.utils.post( { "ReservationID" : alloc["iRes"] }, "checkReservation", alloc["port"], alloc["addr"])
             if "result" not in ret:
                raise Exception("Error in checking reservation: ", str(ret))
             
             instances = ret["result"]["Instances"]
             
             for i in instances:                
                addrs.extend(instances[i]["Address"])
                status = instances[i]["Ready"]
                if type(status) is bool:
                   status = "TRUE"
                ready = ready and status.upper() == "TRUE"
          if ready:
             check_result["Instances"][reservation] = { "Ready": "True", "Address": addrs }
          else:
             check_result["Instances"][reservation] = { "Ready": "False" }      
       return check_result       

    ###############################################  release reservation ############   
    def _release_reservation(self, reservations):
       for reservation in reservations:
          if reservation not in ReservationsView.reservations: 
             raise Exception("cannot find reservation: " + reservation)
          
          data = ReservationsView.reservations[reservation]
          del ReservationsView.reservations[reservation] 
          for alloc in data:
    
             ret = hresman.utils.delete_( { "ReservationID" : alloc["iRes"] }, "releaseReservation", alloc["port"], alloc["addr"])
             #if "result" not in ret:
             #   raise Exception("Error in deleting reservation: ", str(ret))
  
                
       return { }   

    ###############################################  release all reservations ############        
    def _release_all_reservations(self):
       managers = CRSManagersView.managers
       for m in managers:
          hresman.utils.delete_({}, "releaseAllReservations", managers[m]['Port'], managers[m]['Address'])
       ReservationsView.reservations = {}
       return {}           
                   
                      

