#!/usr/bin/env python

import deps
import json

from flask.ext.classy import FlaskView, route
from flask import request
from hresman.utils import json_request, json_reply, json_error
from hresman.resources_view import ResourcesView
import crs_managers_view  
from time import sleep
from hresman import utils
import uuid
import copy

class CRSResourcesView(ResourcesView):
    resources = {}
    
    ################################  get allocation specification ##############  
    def get_alloc_spec(self):
       return 
    
    ################################ request resources from a resource manager ##############
    @route(ResourcesView.version + '/' + ResourcesView.base + '/<id>/request', methods=["POST"])
    def request_resources_id(self, id):
       try:
          if not id in crs_managers_view.CRSManagersView.managers:
             raise Exception("cannot find manager: " + id)
          data = crs_managers_view.CRSManagersView.managers[id]
          try:   
             out = utils.get(crs_managers_view.CRSManagersView.version + '/' + "resources", data["Port"], data["Address"])
             if "result" in out:
                 CRSResourcesView.resources[data["ManagerID"]] = out["result"]
          except Exception as e:
             crs_managers_view.CRSManagersView().delete_manager(data["ManagerID"])
             return json_error(e)
          return json_reply({})
       except Exception as e:          
          return json_error(e)

    ################################ request resources from all IRMs ############
    @route(ResourcesView.version + '/' + ResourcesView.base + '/request', methods=["POST"])
    def request_resources(self):
       try:
          managers = copy.copy(crs_managers_view.CRSManagersView.managers)
          for id in managers:          
             self.request_resources_id(id)
          return json_reply({})
       except Exception as e:
          return json_error(e)

          
