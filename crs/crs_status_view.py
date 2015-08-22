import deps

from flask.ext.classy import FlaskView, route
from flask import  render_template
from hresman.utils import json_request, json_reply, json_error

from crs_managers_view import CRSManagersView
from crs_resources_view import CRSResourcesView
from crs_reservations_view import CRSReservationsView

class CRSStatusView(FlaskView):
    route_base='/'
    addrs = {}
    
    @route("")
    def status(self):      
      try:
         return render_template('index.html')
      except Exception as e:
         return json_error(e)
         
    @route("/data")        
    def status_data(self):      
      try:
         managers = CRSManagersView.managers
         resources = CRSResourcesView.resources
         reservations = CRSReservationsView.reservations
         
         
         ''' reservations -> {'d5937d94-356d-11e5-892f-00505639c717': [{'iRes': [u'f6ab38b5-59a8-44e8-a78e-9c341305d952'], 'sched': {'manager': u'91a19b56-3537-11e5-87b1-00505639c717', 'alloc_req': {u'Attributes': {u'Cores': 1, u'Memory': 200}, u'Type': u'Machine'}, 'res_id': u'vagrant-ubuntu-trusty-64'}, 'addr': '127.0.0.1', 'name': u'IRM-NOVA', 'port': u'8889'}]}
         
         {'Instances': {'199deb52-35c6-11e5-8583-00505639c717': {'Ready': 'True', 'Address': [u'192.168.13.147']}}}

         '''         
         
         for r in reservations:
            if r not in CRSStatusView.addrs:
                  
                  try:
                     ads=CRSReservationsView()._check_reservation([r])
                  except:
                     ads = {"Instances": { r : { "Ready": "True", "Address": ["error"] } } } 
                  if "Instances" in ads:
                     # check that all instances are ready
                     ready = True
                     adsi = ads["Instances"]
                     out_addrs = []
                     for i in adsi:
                        if adsi[i]["Ready"].upper() != "TRUE":
                           ready = False
                           break
                        else:
                           out_addrs.extend(adsi[i]["Address"])

                     if ready:
                        CRSStatusView.addrs[r] = out_addrs 
         print "managers=", str(managers)
         print "resources=", str(resources)
         print "reservations=", str(reservations)
         print "addrs=", str(CRSStatusView.addrs) 
         return json_reply({'managers': managers, 'resources': resources, 'reservations': reservations, 'addrs': CRSStatusView.addrs})
      except Exception as e:
         return json_error(e)    
