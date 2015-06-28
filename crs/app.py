#!/usr/bin/env python

import deps
from flask.ext.classy import FlaskView, route
from flask import  render_template
import threading;
from hresman.manager import HarnessResourceManager
import hresman.utils

import logging

from status_view import StatusView
from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView
from crs_reservations_view import CRSReservationsView
import simple_scheduler
          
crs_views=[CRSManagersView,  \
           StatusView, \
           CRSResourcesView, \
           CRSReservationsView
          ]
          
CRSReservationsView._scheduler=simple_scheduler.schedule

mgr = HarnessResourceManager(crs_views)

def work (): 
  threading.Timer(10, work).start (); 
  try:
     hresman.utils.post({}, 'v3/resources/request', 56789)
  except:
     pass
     
#work()  

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

mgr.run(56789)

   
   

      

  
   

