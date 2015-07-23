#!/usr/bin/env python

import deps

from hresman.metrics_view import MetricsView
import crs_managers_view 
import crs_reservations_view
import copy
from hresman.utils import post

class CRSMetricsView(MetricsView):
    
    ###############################################  create reservation ############ 
    def _get_metrics(self, reservID, address, entry):       
        #managers = copy.copy(crs_managers_view.CRSManagersView.managers)
        reservations = crs_reservations_view.CRSReservationsView.reservations
        
        if reservID not in reservations:
           raise Exception("cannot find reservation: " + reservID)
           
        resData = reservations[reservID]
        
        print resData
        
        for rd in resData:        
           r=post({ "ReservationID": rd['iRes'] }, "checkReservation", rd['port'], rd['addr'])
           if "result" not in r:
              raise Exception("error extracting address from reservationID: ", reservID)
           instances = r["result"]["Instances"]
           
           for i in instances:
              if instances[i]["Ready"].upper() == "FALSE":
                 raise Exception("Reservation: " + i + " not ready!")

              for addr in instances[i]["Address"]:
                 if address == "" or addr == address:
                    print str({ "ReservationID": i, "Address": addr, "Entry": entry })
                    r=post({ "ReservationID": i, "Address": addr, "Entry": entry }, "getMetrics",\
                           rd['port'], rd['addr'])
                    if "result" not in r:
                       raise Exception("Cannot get metrics: " + str(r))       
                    return r["result"]       
        
        raise Exception("Cannot find address for reservation: " + reservID) 
                 

