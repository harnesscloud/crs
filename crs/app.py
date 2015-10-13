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
                  
def request_resources(): 
  global options
  threading.Timer(6.0, request_resources).start (); 
  try:
     hresman.utils.get('v3/resources/request', options.PORT)
  except:
     pass
          
request_resources() 
log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)


CRSReservationsView._select_scheduler(options.scheduler)

print "Using scheduler: %s" % options.scheduler
mgr.run(options.PORT)

   
   

      

  
   

