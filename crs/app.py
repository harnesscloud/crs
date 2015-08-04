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
          
CRSReservationsView._scheduler=simple_scheduler.schedule

mgr = HarnessResourceManager(crs_views)

parser = OptionParser()
parser.add_option("-p", "--port", dest="PORT", default=56788,
                  help="CRS port", type="int")

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

mgr.run(options.PORT)

   
   

      

  
   

