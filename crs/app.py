#!/usr/bin/env python

import deps
from flask.ext.classy import FlaskView, route
from flask import  render_template

from hresman.manager import HarnessResourceManager

from status_view import StatusView
from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView

          
crs_views=[CRSManagersView,  \
           StatusView, \
           CRSResourcesView \
          ]

mgr = HarnessResourceManager(crs_views)
app = mgr.app

@app.template_filter('res_id')
def res_id(id):
   ids = id.split('/')    
   return ids[len(ids)-1]
       
mgr.run(56789)

   
   

      

  
   

