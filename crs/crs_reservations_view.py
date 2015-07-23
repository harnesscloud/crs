#!/usr/bin/env python

import deps

from flask.ext.classy import FlaskView, route
from flask import request

import hresman.utils

from hresman.utils import json_request, json_reply, json_error
from hresman.reservations_view import ReservationsView
from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView
from crs_managers_view import CRSManagersView
import uuid

class CRSReservationsView(ReservationsView):
    _scheduler=None
    ###############################################  create reservation ############ 
    def _create_reservation(self, alloc_req, constraints, monitor):
       schedule = CRSReservationsView._scheduler(CRSManagersView.managers, CRSResourcesView.resources, alloc_req, constraints) 
       
       iResIDs = []
       rollback = False
       for s in schedule:          
          addr = CRSManagersView.managers[s["manager"]]['Address']
          port = CRSManagersView.managers[s["manager"]]['Port']
          rtype = s["alloc_req"]["Type"]
          monitor_data = {}
          if rtype in monitor:
             monitor_data[rtype] = monitor[rtype]
             if "PollTime" in monitor:
                monitor_data["PollTime"] = monitor["PollTime"]
          else:
             monitor_data = {}
                
          data = { "Allocation" : [{ "Type": rtype, \
                                    "ID": s["res_id"], \
                                    "Attributes": s["alloc_req"]["Attributes"] }], \
                   
                   "Monitor": monitor_data
                 } 
          
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
             iResIDs.append({"addr": addr, "port": port, "iRes": ret["result"]["ReservationID"], "sched": s})
       
       if not rollback:
          resID = uuid.uuid1()
          ReservationsView.reservations[str(resID)] = iResIDs
       else:
          for iResID in iResIDs:
             data = {"ReservationID": iResID["iRes"]}
             try:
                hresman.utils.delete(data, 'v3/reservations', iResID["port"], iResID["addr"])
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
          addrs = []
          for alloc in data:
             ret = hresman.utils.post( { "ReservationID" : alloc["iRes"] }, "checkReservation", alloc["port"], alloc["addr"])
             if "result" not in ret:
                raise Exception("Error in checking reservation: ", str(ret))
             
             instances = ret["result"]["Instances"]
             
             for i in instances:                
                addrs.extend(instances[i]["Address"])
                ready = ready and instances[i]["Ready"].upper() == "TRUE"
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
          for alloc in data:
    
             ret = hresman.utils.delete_( { "ReservationID" : alloc["iRes"] }, "releaseReservation", alloc["port"], alloc["addr"])
             if "result" not in ret:
                raise Exception("Error in deleting reservation: ", str(ret))
             
          del ReservationsView.reservations[reservation]       
       return { }   

    ###############################################  release all reservations ############        
    def _release_all_reservations(self):
       managers = CRSManagersView.managers
       for m in managers:
          hresman.utils.delete_({}, "releaseAllReservations", managers[m]['Port'], managers[m]['Address'])
       reservations = ReservationsView.reservations.keys()
       return self._release_reservation(reservations)           
                   
                      

