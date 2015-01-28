#!/usr/bin/env python
from flask import Flask, request, render_template
from time import sleep

from crs_engine import scheduler,logger,log
import json, sys

webserver = Flask(__name__)

needs_refresh = False

@webserver.template_filter('res_id')
def res_id(id):
    ids = id.split('/')    
    return ids[len(ids)-1]
    
def run_webserver(hostname, port):
    # hostname = config.get("SchedulerManager", "HOSTNAME")
    # port = int(config.get("SchedulerManager", "PORT"))  
    webserver.run(host=hostname, port=int(port), debug=False)

#@webserver.before_request
#def beforeRequest():    
#    if "application/json" not in request.headers["Content-Type"]:
#        msg = "Unsupported media type(%s), use application/json" % request.headers["Content-Type"]
#        webserver.logger.error(msg)
#        return msg

@webserver.route("/status/")
def status():
   try:
      IRMs = scheduler.IRMs
      Reservations = scheduler.reservations
      #index_res = filter(lambda i:"InfrastructureReservationIDs" in dir(Reservations[i]), sorted(Reservations.keys(), reverse=True))
      index_res = sorted(Reservations.keys(), reverse=True)
      return render_template('index.html', IRMs=IRMs, RES=Reservations, INDEX_RES=index_res)
   except Exception, msg:
      print "[x] ", str(msg)
       

@webserver.route("/method/addManager", methods=["POST"])
def addManager():
    log("COMM|CRS-REQ|addManager|" + request.data)
    result = json.dumps({"result":scheduler.addManager(json.loads(request.data), request.remote_addr)})
    log("COMM|CRS-RET|addManager|" + result)
    return result
    
@webserver.route("/method/getResourceTypes", methods=["POST"])
def getResourceTypes():
    log("COMM|CRS-REQ|getResourceTypes|" + request.data)
    result = json.dumps({"result":scheduler.getResourceTypes()})
    log("COMM|CRS-RET|getResourceTypes|" + result)    
    return result
    
@webserver.route("/method/prepareReservation", methods=["POST"])
def prepareReservation():
    try:
       log("COMM|CRS-REQ|prepareReservation|" + request.data)
       result = json.dumps({"result":scheduler.prepareReservation(json.loads(request.data))})
       log("COMM|CRS-RET|prepareReservation|" + result) 
       return result
    except Exception, msg:
		return { "error: ", str(msg) }	 

@webserver.route("/method/discardConfiguration", methods=["POST"])
def discardConfiguration():
    log("COMM|CRS-REQ|discardConfiguration|" + request.data)
    result = json.dumps({"result":scheduler.discardConfiguration(json.loads(request.data))})
    log("COMM|CRS-RET|discardConfiguration|" + result) 
    return result
        
@webserver.route("/method/createReservation", methods=["POST"])
def createReservation():
    log("COMM|CRS-REQ|createReservation|" + request.data)
    result = json.dumps({"result":scheduler.createReservation(json.loads(request.data))})
    log("COMM|CRS-RET|createReservation|" + result) 
    return result

@webserver.route("/method/checkReservation", methods=["POST"])
def checkReservation():
    log("COMM|CRS-REQ|checkReservation|" + request.data)
    result = json.dumps({"result":scheduler.checkReservation(json.loads(request.data))})
    log("COMM|CRS-RET|checkReservation|" + result) 
    return result

@webserver.route("/method/releaseReservation", methods=["POST"])
def releaseReservation():
    log("COMM|CRS-REQ|releaseReservation|" + request.data)
    result = json.dumps({"result":scheduler.releaseReservation(json.loads(request.data))})
    log("COMM|CRS-RET|releaseReservation|" + result) 
    return result
    
@webserver.route("/method/releaseAllReservations", methods=["POST", "GET"])
def releaseAllReservations():
    global needs_refresh
    log("COMM|CRS-REQ|releaseAllReservations|" + request.data)
    result = json.dumps({"result":scheduler.releaseAllReservations({})})
    log("COMM|CRS-RET|releaseAllReservations|" + result) 
    needs_refresh = True
    return result
    
@webserver.route("/method/refresh", methods=["POST", "GET"])
def refresh():
    log("COMM|CRS-REQ|refresh|" + request.data)
    result = json.dumps({"result":scheduler.refresh_resources()})
    log("COMM|CRS-RET|refresh|" + result) 
    return result
              
if __name__ == "__main__":
    global CRS_HOST, CRS_PORT
    if len(sys.argv) == 3:
        run_webserver(sys.argv[1], sys.argv[2])
        CRS_HOST=sys.argv[1]
        CRS_PORT=sys.argv[2]
    else:
        CRS_HOST='0.0.0.0'
        CRS_PORT='56789'
    
    run_webserver(CRS_HOST, CRS_PORT)


