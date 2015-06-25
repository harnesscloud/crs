import deps

from flask.ext.classy import FlaskView, route
from flask import  render_template
from hresman.utils import json_request, json_reply, json_error

from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView
class StatusView(FlaskView):
    route_base='/'
    
    @route("/status/")
    @route("/status")
    def status(self):      
      try:
         managers = CRSManagersView.managers
         resources = CRSResourcesView.resources
         return render_template('index.html', MANAGERS=managers, RESOURCES=resources)
      except Exception as e:
         return json_error(e)
         
    @route("/status/data")        
    def status_data(self):      
      try:
         managers = CRSManagersView.managers
         resources = CRSResourcesView.resources
         return json_reply({'managers': managers, 'resources': resources})
      except Exception as e:
         return json_error(e)    
