#!/usr/bin/env python
from flask import Flask, request, render_template
from time import sleep

from crs_engine import scheduler
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
#    print "\n================="
#    print "URL: addManager"
#    print "BODY:", request.data
    result = json.dumps({"result":scheduler.addManager(json.loads(request.data), request.remote_addr)})
#    print "\n================="
#    print "URL: addManager"
#    print "RESULT:"
    return result
    
@webserver.route("/method/getResourceTypes", methods=["POST"])
def getResourceTypes():
#    print "\n================="
#    print "URL: getResourceTypes"
#    print "BODY:", request.data
    # "result:" is already included in the reply of IRM
    result = json.dumps({"result":scheduler.getResourceTypes()})
#    print "\n================="
#    print "URL: getResourceTypes"
#    print "RESULT:", result
    return result
    
@webserver.route("/method/prepareReservation", methods=["POST"])
def prepareReservation():
    try:
		 print "\n================="
		 print "URL: prepareReservation"
		 print "BODY:", request.data
		 result = json.dumps({"result":scheduler.prepareReservation(json.loads(request.data))})
		 print "\n================="
		 print "URL: prepareReservation"
		 print "RESULT:", result
		 return result
    except Exception, msg:
		return { "error: ", str(msg) }	 

@webserver.route("/method/discardConfiguration", methods=["POST"])
def discardConfiguration():
    print "\n================="
    print "URL: discardConfiguration"
    print "BODY:", request.data
    result = json.dumps({"result":scheduler.discardConfiguration(json.loads(request.data))})
    print "\n================="
    print "URL: discardConfiguration"
    print "RESULT:", result
    return result
        
@webserver.route("/method/createReservation", methods=["POST"])
def createReservation():
    print "\n================="
    print "URL: createReservation"
    print "BODY:", request.data
    result = json.dumps({"result":scheduler.createReservation(json.loads(request.data))})
    print "RESULT:", result
    return result

@webserver.route("/method/checkReservation", methods=["POST"])
def checkReservation():
    print "\n================="
    print "URL: checkReservation"
    print "BODY:", request.data
    result = json.dumps({"result":scheduler.checkReservation(json.loads(request.data))})
    print "RESULT:", result
    return result

@webserver.route("/method/releaseReservation", methods=["POST"])
def releaseReservation():
    print "\n================="
    print "URL: releaseReservation"
    print "BODY:", request.data
    result = json.dumps({"result":scheduler.releaseReservation(json.loads(request.data))})
    print "\n================="
    print "URL: releaseReservation"
    print "RESULT:", result
    return result
    
@webserver.route("/method/releaseAllReservations", methods=["POST", "GET"])
def releaseAllReservations():
    global needs_refresh
    print "\n================="
    print "URL: releaseAllReservations"
    print "BODY:", request.data
    result = json.dumps({"result":scheduler.releaseAllReservations({})})
    print "\n================="
    print "URL: releaseAllReservations"
    print "RESULT:", result
    needs_refresh = True
    return result
    
@webserver.route("/method/refresh", methods=["POST", "GET"])
def refresh():
    result = json.dumps({"result":scheduler.refresh_resources()})
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


