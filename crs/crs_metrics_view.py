#!/usr/bin/env python

import deps

from hresman.metrics_view import MetricsView
import crs_managers_view 
import crs_reservations_view
import copy
from hresman.utils import post, json_request, json_reply, json_error
import random

from flask.ext.classy import FlaskView, route
import json
import time


class CRSMetricsView(MetricsView):
    
    ###############################################  getMetrics ############ 
    def _get_metrics(self, reservID, address, entry):       
        #managers = copy.copy(crs_managers_view.CRSManagersView.managers)
        reservations = crs_reservations_view.CRSReservationsView.reservations
        
        if reservID not in reservations:
           raise Exception("cannot find reservation: " + reservID)
           
        resData = reservations[reservID]
        print "resData=", json.dumps(resData, indent=4) 
        ret = {}
        for rd in resData:        
           r=post({ "ReservationID": rd['iRes'] }, "checkReservation", rd['port'], rd['addr'])
           if "result" not in r:
              raise Exception("error extracting address from reservationID: ", reservID)
              
           print "r['result'] =", json.dumps(r["result"], indent=4)    
           instances = r["result"]["Instances"]
           
           for i in instances:
              status = instances[i]["Ready"]
              if type(status) is bool:
                  status = "TRUE"
              if status.upper() == "FALSE":
                 raise Exception("Reservation: " + i + " not ready!")

              for addr in instances[i]["Address"]:
                 if address == "" or addr == address:
                    print str({ "ReservationID": i, "Address": addr, "Entry": entry })
                    r=post({ "ReservationID": i, "Address": addr, "Entry": entry }, "getMetrics",\
                           rd['port'], rd['addr'])
                    if "result" not in r:
                       raise Exception("Cannot get metrics: " + str(r))       
                    ret[addr] = r["result"]["Metrics"]
        return { "Metrics": ret }    
        
        raise Exception("Cannot find address for reservation: " + reservID) 
                 

    ########################################  mock-up getMetrics ############ 
    
    dummy_metrics = {}
    size_series = 1000
    
    @staticmethod
    def create_csv(series, timestamp, entry, nitems):
       i = 0
       csv = ""
       while i < nitems:
          if csv == "":
             csv = "%s,%s,%.2f\n" % (entry+1, timestamp+entry,series[entry])
          else: 
             csv += ",%s,%s,%.2f\n" % (entry+1, timestamp+entry,series[entry]) 
          i += 1
          entry +=1 
       return csv
       

    @route('/getMetrics2', methods=["POST"])         
    def get_metrics_dummy(self):
       try:
          in_data = json_request()
         
          reservID = in_data['ReservationID']    
          if "Address" not in in_data:
             addr = ""
          else:       
             addr = in_data['Address']
          if 'Entry' not in in_data:
             entry = 0
          else:
             entry = in_data['Entry']-1
          
          if entry < 0 or entry >=CRSMetricsView.size_series:
             raise Exception("invalid entry: %d" % (entry+1)) 
          
                  
          if addr not in CRSMetricsView.dummy_metrics:
             lst = addr.split(':')
             if len(lst) == 3 and lst[1].isdigit() and lst[2].isdigit():              
                mean = int(lst[1])
                std = int(lst[2])
             else:
                mean = 10
                std = 3
             series1 = [0]*CRSMetricsView.size_series
             series2 = [0]*CRSMetricsView.size_series             
             for i in range(0, CRSMetricsView.size_series):   
                series1[i] = random.gauss(mean, std)
                series2[i] = random.gauss(mean, std)
             CRSMetricsView.dummy_metrics[addr] = {"series1":  series1, "series2": series2, "timestamp": time.time() }
  
          timestamp = CRSMetricsView.dummy_metrics[addr]["timestamp"]         
          
          series1 = CRSMetricsView.dummy_metrics[addr]["series1"]   
          nitems1 = random.randint(0,9)
          if nitems1 + entry < CRSMetricsView.size_series:
              nitems1 
          csv1 = CRSMetricsView.create_csv(series1, timestamp, entry, nitems1)     
          
          series2 = CRSMetricsView.dummy_metrics[addr]["series2"]   
          nitems2 = random.randint(0,9)
          csv2 = CRSMetricsView.create_csv(series2, timestamp, entry, nitems2)             
          return json_reply({"Metrics": { "METRIC1": csv1, "METRIC2": csv2 }}) 
                            
       except Exception as e:           
          return json_error(e)    
