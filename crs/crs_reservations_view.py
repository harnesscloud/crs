#!/usr/bin/env python

import deps

from flask.ext.classy import FlaskView, route
from flask import request

from hresman.utils import json_request, json_reply, json_error, post, delete
from hresman.reservations_view import ReservationsView
from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView

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
             ret = post(data, 'v3/reservations', port, addr)
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
                delete(data, 'v3/reservations', iResID["port"], iResID["addr"])
             except:
                pass  
          raise Exception("cannot make reservation! (rollbacking)")  
             
       return { "ReservationID" : [str(resID)] }                    
    
    ###############################################  check reservation ############   
    def _check_reservation(self, reservations):
       raise Exception("check reservation method has not been implemented!")
       
           
    ###############################################  release reservation ############   
    def _release_reservation(self, reservations):
       raise Exception("release reservation method has not been implemented!")
                   
                      

