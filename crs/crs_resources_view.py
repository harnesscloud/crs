#!/usr/bin/env python

from hresman import utils
from hresman.utils import json_request, json_reply, json_error
from hresman.resources_view import ResourcesView
import crs_managers_view 
import copy
from hresman.utils import get

class CRSResourcesView(ResourcesView):
     ################################  get allocation specification ##############  
    def _get_alloc_spec(self):
        managers = copy.copy(crs_managers_view.CRSManagersView.managers)
        types = {}
        constraints = {}
        agg = {}
        metrics = {}
        
        for id in managers:          
           ret = get("getAllocSpec", managers[id]["Port"], managers[id]["Address"])
           if "result" in ret:
              spec = ret["result"]
              if ("Monitor" in spec) and ("Metrics" in spec["Monitor"]):
                 metrics.update(spec["Monitor"]["Metrics"])
              if ("Types" in spec):    
                 types.update(spec["Types"])
                 
        return { "Types": types, "Constraints":  constraints, "Monitor": { "Metrics": metrics, \
                                                                           "Aggregation": agg } }
                                                                           
