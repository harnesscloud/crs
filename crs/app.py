#!/usr/bin/env python

import deps
from flask.ext.classy import FlaskView, route
from flask import  render_template
import threading;
from hresman.manager import HarnessResourceManager
import hresman.utils
import logging
from optparse import OptionParser

from crs_status_view import CRSStatusView
from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView
from crs_reservations_view import CRSReservationsView
from crs_metrics_view import CRSMetricsView
from crs_cost_view import CRSCostView
import simple_scheduler
          
crs_views=[CRSManagersView,  \
           CRSStatusView, \
           CRSMetricsView, \
           CRSResourcesView, \
           CRSReservationsView,
           CRSCostView
          ]
          
mgr = HarnessResourceManager(crs_views)

parser = OptionParser()
parser.add_option("-p", "--port", dest="PORT", default=56788,
                  help="CRS port", type="int")
parser.add_option("-s", "--scheduler", dest="scheduler", default="simple",
                  help="CRS scheduler ('simple', 'NC')", type="string")                  

(options,_) = parser.parse_args()
                  
def work (): 
  global options
  threading.Timer(10, work).start (); 
  try:
     hresman.utils.post({}, 'v3/resources/request', options.PORT)
  except:
     pass
          
#work()  
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if options.scheduler == "simple":
   import simple_scheduler
   CRSReservationsView._scheduler=simple_scheduler.schedule
elif options.scheduler == "NC":
   import schedulerNC
   CRSReservationsView._scheduler=schedulerNC.schedule
else:
    raise Exception("invalid scheduler: %s" % options.scheduler)

print "Using scheduler: %s" % options.scheduler
mgr.run(options.PORT)

   
   

      

  
   

