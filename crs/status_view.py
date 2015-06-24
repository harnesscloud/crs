import deps

from flask.ext.classy import FlaskView, route
from flask import  render_template
from hresman.utils import json_request, json_reply, json_error

from crs_managers_view import CRSManagersView

class StatusView(FlaskView):
    route_base='/'
    
    @route("/status/")
    @route("/status")
    def status(self):      
      try:
         irms = CRSManagersView.managers
         return render_template('index.html', IRMs=irms, RES={}, INDEX_RES={})
      except Exception as e:
         return json_error(e)
