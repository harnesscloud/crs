#!/usr/bin/env python
from flask import Flask, request
from scheduler import scheduler
import json, sys
# from httplib import NotConnected

webserver = Flask(__name__)

def run_webserver(hostname, port):
    # hostname = config.get("SchedulerManager", "HOSTNAME")
    # port = int(config.get("SchedulerManager", "PORT"))  
    webserver.run(host=hostname, port=int(port), debug=False)

@webserver.before_request
def beforeRequest():    
    if "application/json" not in request.headers["Content-Type"]:
        msg = "Unsupported media type(%s), use application/json" % request.headers["Content-Type"]
        webserver.logger.error(msg)
        return msg

@webserver.route("/method/addManager", methods=["POST"])
def addManager():
    print "\n================="
    print "URL: addManager"
    print "BODY:", request.data
    result = json.dumps({"result":scheduler.addManager(json.loads(request.data))})
    print "\n================="
    print "URL: addManager"
    print "RESULT:"
    return result
    
@webserver.route("/method/getResourceTypes", methods=["POST"])
def getResourceTypes():
    print "\n================="
    print "URL: getResourceTypes"
    print "BODY:", request.data
    # "result:" is already included in the reply of IRM
    result = json.dumps({"result":scheduler.getResourceTypes()})
    print "\n================="
    print "URL: getResourceTypes"
    print "RESULT:", result
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

if __name__ == "__main__":
    if len(sys.argv) == 3:
        run_webserver(sys.argv[1], sys.argv[2])
    else:
        run_webserver("localhost", "5558")
        #run_webserver("131.254.201.5", "5558")
        #run_webserver("172.16.0.1", "5558")
