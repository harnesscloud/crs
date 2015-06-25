#!/usr/bin/env python

import deps

from flask.ext.classy import FlaskView, route
from flask import request

from hresman.utils import json_request, json_reply, json_error
from hresman.reservations_view import ReservationsView
from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView

class CRSReservationsView(ReservationsView):
    _scheduler=None
    ###############################################  create reservation ############ 
    def _create_reservation(self, alloc_req, constraints, monitor):
       CRSReservationsView._scheduler(CRSManagersView.managers, CRSResourcesView.resources, alloc_req, constraints) 
       return {}                   
    
    ###############################################  check reservation ############   
    def _check_reservation(self, reservations):
       raise Exception("check reservation method has not been implemented!")
       
           
    ###############################################  release reservation ############   
    def _release_reservation(self, reservations):
       raise Exception("release reservation method has not been implemented!")
                   
                      

