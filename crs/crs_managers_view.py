#!/usr/bin/env python

import deps
from hresman.managers_tree_view import ManagersTreeView
from threading import Timer
from crs_resources_view import CRSResourcesView

class CRSManagersView(ManagersTreeView): 
    ###############################################  register manager ##############
    def _registerManager(self, data):
       Timer(2, CRSResourcesView().request_resources_id, args=[data["ManagerID"]]).start()
       

       
       
             
