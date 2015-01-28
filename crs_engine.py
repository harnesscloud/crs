#!/usr/bin/env python
import json, requests, sys, uuid, socket
from threading import Thread, Lock
import operator
import logging
import logging.handlers as handlers

#Config and format for logging messages
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)d - %(levelname)s: %(filename)s - %(funcName)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
handler = handlers.TimedRotatingFileHandler("crs.log",when="H",interval=24,backupCount=0)
## Logging format
handler.setFormatter(formatter)
logger.addHandler(handler)

def log(msg):
   logger.info(msg)
   print "[i] " + msg 

def harness_request(topic, sender, receiver, msg):
   sender=sender.replace('-','_') 
   receiver=receiver.replace('-','_')
   logger.info("SEQ:" + topic + "||" + sender + "->" + receiver + ": " + msg)
   
def harness_reply(topic, sender, receiver, msg):
   sender=sender.replace('-','_')
   receiver=receiver.replace('-','_')
   logger.info("SEQ:" + topic + "||" + sender + "-->>" + receiver + ": " + msg)

def harness_note(topic, component, msg):
   component=component.replace('-','_')
   logger.info("SEQ:" + topic + "||" + "note over " + component + ": " + msg)

   
class Connection(object):
    """This is a wrapper for http connections"""
    
    def __init__(self, data):
       self.URL = "http://" + data["Hostname"] + ":" + str(data["Port"])
        
    def requestPost(self, url, body):
        try:  
            #self.conn.request("POST", "/method" + url, json.dumps(body), {"Content-type":"application/json"})         
            #response = self.conn.getresponse()
            log("COMM|IRM-REQ|" + url + "|" + str(json.dumps(body)))
            result = requests.post(self.URL + "/method" + url, json.dumps(body), headers={'content-type': 'application/json'})
        except Exception, msg:
            print "HTTPConnection request problem: ", msg, url, body
            raise Exception("HTTPConnection request problem", url, body)  
        response = result.text
        log("COMM|IRM-RET|" + url + "|" + response)
        #print "\n*****************"
        print "URL:", url, "\nRESPONSE:",  response
        return response
    
# ==============================================================

class Resource:
    def __init__(self, data, irm={}):
        for key in data:
            self.__dict__[key] = data[key]
        self.data = data
        self.irm = irm
    
    def getType(self):
       return self.Type
        

    def getJson_calculateResource(self):
        d = { "Type" : self.__dict__["Type"], "Attributes" : self.__dict__["Attributes"] }
        return d
    
    def getJson_reserveResources(self):
        return { "ID" : self.__dict__["ID"], "IP" : self.__dict__["IP"], "Type" : self.__dict__["Type"], "Attributes" : self.__dict__["Attributes"] }
        
    
'''
# ==============================================================          

class Rack:    
    def __init__(self, ID, datacenter):
        self.ID = ID
        self.resources = {}
        self.resourcesTotal = {}
        self.type_irm = {} 
        self.irm_resources = {} 
        self.datacenter = datacenter
        self.distances = {}
        
    def addResource(self, data, irm):
        resource = Resource(data)
        resource.irm = irm
        resource.distances = {}
        self.resources[data["ID"]] = resource
        
        if resource.getType() not in self.type_irm.keys():
            self.type_irm[resource.getType()] = resource.irm 
        if resource.getType() not in self.datacenter.type_irm.keys():
            self.datacenter.type_irm[resource.getType()] = resource.irm 
        if irm.ID not in self.irm_resources.keys():
            self.irm_resources[irm.ID] = { }
        self.irm_resources[irm.ID][data["ID"]] = resource
                 
    def calculateResourceAgg(self):
        resources = {}
        for resource in self.resources.values():
            if resource.getType() not in resources.keys():
                resources[resource.getType()] = { "Resources" : [] }
            resources[resource.getType()]["Resources"].append(resource.getJson_calculateResource())
        for type_ in resources:
            data = self.type_irm[type_].conn.requestPost("/calculateResourceAgg", resources[type_])
            data = json.loads(data)
            self.resourcesTotal[type_] = data["result"]
        pass

    def satisfy(self, data):
        resource = None
        for r in self.resources.values():
            if r.satisfy(data):
                resource = r
                break
        return resource


	def update_TotalResources(self, toadd = {}, tosubstract={}):
		for key in toadd:
			for k in self.resourcesTotal[key]["Attributes"]:
				self.resourcesTotal[key]["Attributes"][k] = self.resourcesTotal[key]["Attributes"][k] + toadd[key][k]
			
		for key in tosubstract:
			for k in self.resourcesTotal[key]["Attributes"]:
				self.resourcesTotal[key]["Attributes"][k] = self.resourcesTotal[key]["Attributes"][k] - tosubstract[key][k]
			
		
# ==============================================================          

class DataCenter:
    def __init__(self, ID):
        self.ID = ID
        self.racks = {}
        self.distances = {}
        self.resourcesTotal = {}
        self.type_irm = {} 
        
    def calculateResourceAgg(self):
        resources = {}
        for rack in self.racks.values():
            for k, v in rack.resourcesTotal.items():
                if k not in resources.keys():
                    resources[k] = { "Resources" : [] }
                resources[k]["Resources"].append(v)
        for type_ in resources:
            data = self.type_irm[type_].conn.requestPost("/calculateResourceAgg", resources[type_])
            data = json.loads(data)
            self.resourcesTotal[type_] = data["result"]
        
    
    def satisfy(self, data):
        resource = None
        for rack in self.racks.values():
            resource = rack.satisfy(data)
            if resource is not None:
                break
        return resource
'''    
# ==============================================================

class IRM:
    def __init__(self, data, remote_ip):

        host, _, _ = socket.gethostbyaddr(remote_ip)
        self.ID = host + ":" + str(data["Port"])
  
        self.Resources = { }
        self.Hostname = data["Hostname"]
        self.Port = data["Port"]
        if "Name" in data:
           self.Name = data["Name"]
        else:
           self.Name = "<unknown>"
                
        self.conn = Connection(data)
        
    def getResourceTypes(self):
        data = self.conn.requestPost("/getResourceTypes", {})
        data = json.loads(data)
        data = data["result"]["Types"]
        return data
                  
    
    def getAvailableResources(self):
        data = self.conn.requestPost("/getAvailableResources", {})
        harness_request("Discovery", "CRS", self.Name, "Get available resources")
        data = json.loads(data)
        data = data["result"]
    
        set_IPs = set()
        set_Types = set()

        for d in data["Resources"]:
           self.Resources[d["ID"]] = Resource(d, self)
           set_IPs.add(d["IP"])
           set_Types.add(d["Type"])

        harness_reply("Discovery",  self.Name, "CRS", str(set_Types).replace('set', '') + ":" + 
                      str(set_IPs).replace('set',''))         
            
# ==============================================================

class Reservation:
	id_reservation_max = 0 # variable used for reservation number management
	id_reservations = [] # available reservation number candidates for newly received reservations

	def __init__(self, data={}):              
		self.id_ = self.getIdReservation()
		self.requests = {}
		self.aggregatedResources = {}
		self.distanceSpecified = False

		for d in data["Resources"]:
			if "GroupID" not in d:
				d["GroupID"] = "G" + os.urandom(5)
			if "NumInstances" not in d:
				d["NumInstances"] = 1
			self.requests[d["GroupID"]] = Resource(d)
			self.requests[d["GroupID"]].distance = sys.maxint
			if "Image" in d:	
				self.requests[d["GroupID"]].Image = d["Image"]
			if "UserData" in d:
				self.requests[d["GroupID"]].UserData = d["UserData"]
			if not (d["Type"] in self.aggregatedResources):
				self.aggregatedResources[d["Type"]] = self.aggregate_res_description({}, d["Attributes"], d["NumInstances"])
			else:
				self.aggregatedResources[d["Type"]] = self.aggregate_res_description(self.aggregatedResources[d["Type"]], d["Attributes"], d["NumInstances"])
		
		if 'Distances' in data:
			self.distanceSpecified = True
			for d in data["Distances"]:
				if self.requests[d["Source"]].distance > d["NumHops"]:  
					self.requests[d["Source"]].distance = d["NumHops"]        
				if self.requests[d["Target"]].distance > d["NumHops"]:  
					self.requests[d["Target"]].distance = d["NumHops"]

	def aggregate_res_description(self, data = {}, toadd = {}, num = 1):
		for key in toadd:
			if key in data:
				data[key] = data[key] + (toadd[key] * num)
			else:
				data[key] = toadd[key] * num
		return data
		
	def __del__(self):
		self.__class__.id_reservations.append(self.id_)

	def getIdReservation(self):
		id_ = self.__class__.id_reservation_max
		if self.__class__.id_reservations:
			# if there are available IDs, then return the min id value and remove this id value from id_trees 
			id_ = min(self.__class__.id_reservations)
			self.__class__.id_reservations.remove(id_)
		else:
			# if there is not any available id, then increase the max tree id by one, and return this value
			self.__class__.id_reservation_max = self.__class__.id_reservation_max + 1
		return id_

	def getResultPrepareReservation(self):
		result = { "ConfigID" : str(self.id_)}
		resources = []
		print "Prepare response to prepare configuration...."
		for groupid in self.requests:
			for i in range(self.requests[groupid].NumInstances):
			   x = self.requests[groupid].getJson_calculateResource()
			   x["GroupID"] = groupid
			   resources.append(x)				
		result["Resources"] = resources
		return result

	def getJson_reserveResources(self):
		request = self.requests.values()[0]
		resource = request.resource
		d = { "ID" : resource.ID, "IP" : resource.IP, "Type" : resource.Type, "Attributes" : request.Attributes }
		if hasattr(request, 'Image'):
			d['Image'] = request.Image
		if hasattr(request, 'UserData'):
			d['UserData'] = request.UserData
		return d
		# return { 
		#             "ID" : resource.ID, \
		#             "IP" : resource.IP, \
		#             "Type" : resource.Type, \
		#             "Attributes" : request.Attributes
		#         }
    
# ==============================================================          

class Scheduler:
    def __init__(self):
        self.IRMs = { }
        self.reservations = {}
        harness_note("Discovery", "CRS", "Ready!")
        with open('crs.constraints') as f:
          try:
             self.constraints = json.load(f)
          except AttributeError:
             self.constraints = {  }
             pass

    def __del__(self):
        pass

    def addManager(self, data, remote_ip):
        if data["Manager"] == "IRM":
            irm = IRM(data, remote_ip)
            self.IRMs[irm.ID] = irm
            log("Adding IRM: " + irm.Name + "( " + remote_ip + ")")

            harness_reply("Discovery", irm.Name, "CRS", "Register " + irm.Name.replace("-","_"))
            Thread(target=self.getDelayAvailableResources, args=[irm.ID]).start()

        return {}
    
        
    def getDelayAvailableResources(self, index):
        import time
        
        time.sleep(2)
        self.IRMs[index].getAvailableResources()
           
    def getResourceTypes(self):
        result = { "Types" : [] }
        for irm in self.IRMs:
            r = self.IRMs[irm].getResourceTypes()
            result["Types"].extend(r) 
        return result    
    		
	 # TODO: this should take into account the data types	of the attributes!
    def satisfies(self, available_res = {}, requested_res = {}):
		q = True
		for resType in requested_res:
			for key in requested_res[resType]:
				if available_res[resType]["Attributes"][key] < requested_res[resType][key]:
					q = False
					break 
		return q
		
    def apply_constraints(self, available_ips, requests):       
       if self.constraints == {}:
          return available_ips
       
       # get all types in a request
       types_req = set()
       for r in requests:
          types_req.add(requests[r].Type)
       
       selected_zone = None
       for zone in self.constraints["Zones"]:
          ztypes = set(zone["Types"])
          if (types_req <= ztypes):
             selected_zone = zone
             break
       
       if selected_zone == None:
          raise Exception("cannot find a zone: cannot reserve resources!")
 
       
       ips = filter(lambda x: x != None, map(lambda x: self.constraints["Hosts"].get(x), zone["Hosts"]))
       print "requested types = ", types_req       
       print "selected zone = ", selected_zone["Name"]
       print "selected resources = ", ips
       
       return ips
    
    def prepareReservation(self, data):
		self.refresh_resources()
		reservation = Reservation(data)		
		self.reservations[reservation.id_] = reservation
		candidates = []
		
		
		for i in self.IRMs:               
		   candidates.extend(self.IRMs[i].Resources.values())
		print "::::>" , candidates			
		reserved_res = {}
		# for each rack that has enough resources

		available_ips = map(lambda x: x.IP, candidates)
		print "Resources available = ", available_ips
		
		try:
			ips = self.apply_constraints(available_ips, reservation.requests)
			
			if ips == []:
			   raise Exception("cannot find resources to satisfy this requests!")
			
		
			reserved_res = {}
			cost = 0.0	
			
		   # for each group of requests
			for key in reservation.requests:
				k = 0 				
				i = 0 # instance id
   			
				reserved_res[key] = []				
				# traverse 
				print "num instances = ", reservation.requests[key].NumInstances
				while(i < reservation.requests[key].NumInstances and k < len(ips)):
					print "iteration: ", i, ":", k
               ## list of resources that have IP=ips[k] *and* requested type
					resource = filter(lambda r:r.IP == ips[k] and r.Type == reservation.requests[key].Type, 
					           candidates)
					
					         
					# assumes one IP per type e.g. resource[0]
					if resource == []:
						k = k + 1
						continue
					else:
						resource = resource[0]

					to_substract = []
					
					# set attributes added from previous schedule for this resource (resource.ID)
					expanded_allocations = []					         	
					for allocs in reserved_res.values():
						expanded_allocations.extend(allocs)			
					for j in range(len(expanded_allocations)):
						if expanded_allocations[j]["Allocation"]["ID"] == resource.ID:
							to_substract.append({"Attributes" : expanded_allocations[j]["Allocation"]["Attributes"]})		
					to_substract.append({"Attributes" : reservation.requests[key].Attributes})                                            
					irm_req = {"Resource" : resource.getJson_calculateResource(), "Reserve" : to_substract, "Release" : []}
					#request calculate capacity to irm
					#try:
					result = resource.irm.conn.requestPost("/calculateResourceCapacity", irm_req)                
					#except Exception:
					#	result = {"Resource" : resource.getJson_calculateResource()}                                                
					#	pass

					result = json.loads(result)["result"]					
					if result == {}:
						k = k + 1
						continue
					else:
						alloc_obj = {"ID" : resource.ID, "IP" : resource.IP, \
					               "Type" : resource.Type, \
						            "Attributes" : reservation.requests[key].Attributes}
						if "UserData" in dir(reservation.requests[key]):
						   alloc_obj["UserData"] = reservation.requests[key].UserData
						if "Image" in dir(reservation.requests[key]):
						   alloc_obj["Image"] = reservation.requests[key].Image
											   
						reserved_res[key].append({"Allocation" : alloc_obj, "IRM" : resource.irm})							
						for component in resource.Cost:
							#print "Computing cost resource : ", resource.Cost
							if component in reservation.requests[key].Attributes:
								cost = cost + float(resource.Cost[component]) * float(reservation.requests[key].Attributes[component])
					i = i+1
				if i != reservation.requests[key].NumInstances: 
					raise Exception("Cannot satisfy this request!")
				   						
		except Exception, msg:
			print "ERROR: ", str(msg)
			reserved_res = {}
			pass
		if (reserved_res == {}) or ([] in reserved_res.values()):
			#configuration not found
			return {}
		print "\n----------------------------------------------------"
                
		res = map(lambda r: r["Allocation"], sum(reserved_res.values(),[]))
                sres = ""
		for r in res:
		   print "=>", r["IP"], ":", r["Type"]
                   if sres != "":
                      sres = sres + ";"
                   sres = sres + str(r["Type"]) + ":" + str(r["IP"])
		print "----------------------------------------------------\n"
		try:
			reservation.Allocations = reserved_res
                        harness_note("Reservation", "CRS", "Allocated [ID:" + str(reservation.id_) + "]: " + str(sres))
			result = reservation.getResultPrepareReservation()
			result["Cost"] = cost
			print "Result prepare reservation :", result
		except:
				import traceback
				traceback.print_exc()
		print "prepareReservation done"  
		return result    
    
    def discardConfiguration(self, data):
        result = {}
        return result 
    
       
    def createReservation(self, data):
		id_ = int(data["ConfigID"])
		try:
			reservation = self.reservations[id_]		
			data = []
			allocs = []
			
			for alloc in reservation.Allocations.values():
				allocs.extend(alloc)
				
			for i in range(len(allocs)):
				reserv = allocs[i]["IRM"].conn.requestPost("/reserveResources", {"Resources":[allocs[i]["Allocation"]]})
                                harness_request("Reservation", "CRS", allocs[i]["IRM"].Name, "[ID:" + str(id_) + "] " + str(allocs[i]["Allocation"]["Attributes"]))
				reserv = json.loads(reserv)
				if reserv["result"]["Reservations"] == []:
					raise Exception()
				data.append(reserv["result"]["Reservations"])
                                harness_reply("Reservation", allocs[i]["IRM"].Name, "CRS", "[ID:" + str(id_) + "] reservation: OK!") 
			
			reservation.InfrastructureReservationIDs = data
		except Exception,msg:
			#import traceback
			#traceback.print_exc()
			print "Failed reserving resource: ", msg
			return {}
		return {"ResID":id_}
		 
    def checkReservation(self, data):
      try:
			reservation = self.reservations[int(data["ResID"])]
			allocs = []
			groupIDs = []
			gkeys = reservation.Allocations.keys()
			
			i = 0
			for alloc in reservation.Allocations.values():
				allocs.extend(alloc)
				for j in range(len(alloc)):
				   groupIDs.append(gkeys[i])
				i = i + 1
				
			isready = True
			instances = []
			for i in range(len(allocs)):
				result = allocs[i]["IRM"].conn.requestPost("/verifyResources", {"Reservations":reservation.InfrastructureReservationIDs[i]})
				result = json.loads(result)
				result = result["result"]
				isready = isready and result["Reservations"][0]["Ready"] and "Address" in result["Reservations"][0].keys()
				if isready:
				   instance = {}
				   instance["Address"] = result["Reservations"][0]["Address"] 
				   instance["GroupID"] = groupIDs[i]
				   # to remove, I think
				   if "ID" in result["Reservations"][0]:
				      instance["ID"] = result["Reservations"][0]["ID"]
				   instances.append(instance)
				else:
					return {}
			
			return {"Ready": True, "Instances": instances }
      except Exception,msg:
			print "Failed checking resource: ", msg
			return {}
		
    def releaseReservation(self, data):
  		import time
  		reservation = self.reservations[int(data["ResID"])]
  		allocs = []
  		IRMs={}
		for alloc in reservation.Allocations.values():
			allocs.extend(alloc)
		try:

			for i in range(len(allocs)):
				IRMs[allocs[i]["IRM"]] = True
				result = allocs[i]["IRM"].conn.requestPost("/releaseResources", {"Reservations":reservation.InfrastructureReservationIDs[i]})
				result = json.loads(result)
				if result["result"] != {}:
				   raise Exception("could not remove all resources!")
			return {}      
			  
		except Exception, msg:
			return {"error": str(msg)}
			
    def releaseAllReservations(self, data):
       try:
          for irm in self.IRMs:
             result = json.loads(self.IRMs[irm].conn.requestPost("/releaseAllResources", {}))
          return { }       
       except Exception, msg:
		   return {"error": str(msg)}		
		   
    def refresh_resources(self):
       try:           
          blacklist = []
          for i in self.IRMs:
             try:
                self.IRMs[i].getAvailableResources()
             except:
                 blacklist.append(i)  
          for i in blacklist:
              print "cannot connect to IRM " + self.IRMs[i].ID + "... removing it!"
              self.IRMs.pop(i)
          return { }       
       except Exception, msg:
		   return {"error": str(msg)}		
 	

scheduler = Scheduler() 



