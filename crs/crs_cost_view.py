import deps

from flask.ext.classy import FlaskView, route
from flask import  render_template
from hresman.utils import json_request, json_reply, json_error
import json

import os

class CRSCostView(FlaskView):
    route_base='/'
    
    @staticmethod
    def compute_cost_sub(subconfig):
       if subconfig["Type"] in CRSCostView.pricing:
          price_str = CRSCostView.pricing[subconfig["Type"]]
          for attr in subconfig["Attributes"]:
             value = subconfig["Attributes"][attr]
             price_str = price_str.replace("%" + attr, str(value))
          return eval(price_str) 
       else: 
          return 0

    @staticmethod
    def compute_cost(config):
       return sum (map(CRSCostView.compute_cost_sub, config)) 
    
    @route("/getCost", methods=["POST"])        
    def compute_costs(self):
      CRSCostView.pricing = {}      
      try:
         curr = os.path.dirname(os.path.abspath(__file__))
         with open(curr + '/pricing.cfg') as data_file:    
           CRSCostView.pricing = json.load(data_file)
      except:
         pass
      
      configs = json_request()
      
      try:
         cost = map(CRSCostView.compute_cost, configs["Configurations"])  
         return json_reply(cost) 
      except Exception as e:
         return json_error(e)  
