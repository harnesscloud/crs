#!/usr/bin/env python

import deps
from flask.ext.classy import FlaskView, route
from flask import  render_template
from hresman import manager, managers_view, resources_view, reservations_view, metrics_view
from hresman import utils


           
           
class status_view(FlaskView):
    route_base='/'
    
    @route("/status/")
    @route("/status")
    def status(self):      
      try:
         irms = managers_view.ManagersView.managers
         print "=====>", irms
         return render_template('index.html', IRMs=irms, RES={}, INDEX_RES={})
         #return render_template('index.html')
      except Exception as e:
         return utils.json_error(e)

crs_views=[managers_view.ManagersView,  \
           resources_view.ResourcesView, \
           reservations_view.ReservationsView, \
           metrics_view.MetricsView,
           status_view]


mgr = manager.HarnessResourceManager(crs_views)
app = mgr.app

@app.template_filter('res_id')
def res_id(id):
   ids = id.split('/')    
   return ids[len(ids)-1]
       
mgr.run(56789)

   
   

      

  
   

