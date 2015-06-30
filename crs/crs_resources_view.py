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

class CRSResourcesView(ResourcesView):
     ################################  get allocation specification ##############  
    def get_alloc_spec(self):
       return 
    
 
