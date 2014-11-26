#!/usr/bin/env python
from trest import expect

API="http://localhost:56789"

expect("getResourceTypes", 
       lambda x: ("result" in x) and ("Types" in x["result"]) and (x["result"]["Types"][0]["Type"] == "Storage"), 
       API, "getResourceTypes")

####################################################### prepareReservation
p1 = expect("getSimpleStorageReq1", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Capacity"] == 10, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Storage",
						"NumInstances":1,
						"Attributes":{
			            "Capacity":10,
						   "Throughput": 15,
						   "AccessType": "SEQUENTIAL"
						}
				  }
		   ],
		   "Distances":[]
	    }  
) 

p2 = expect("getSimpleStorageReq2", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Capacity"] == 20, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Storage",
						"NumInstances":1,
						"Attributes":{
			            "Capacity":20,
						   "Throughput": 15,
						   "AccessType": "SEQUENTIAL"
						}
				  }
		   ],
		   "Distances":[]
	    }  
) 

####################################################### createReservation/releaseReservation
r1 = expect("createReservation1", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p1["result"]["ConfigID"]
	    }  
)

expect("checkReservation1", 
        lambda x: x["result"]["Ready"], API, "checkReservation",
       {
			"ResID": r1["result"]["ResID"]
	    }  
)


expect("releaseReservation1", 
        lambda x: x["result"] == {}, API, "releaseReservation",
       {
			"ResID": r1["result"]["ResID"]
	    }  
)


r2 = expect("createReservation2", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p2["result"]["ConfigID"]
	    }  
)  


expect("checkReservation2", 
        lambda x: x["result"]["Ready"], API, "checkReservation",
       {
			"ResID": r2["result"]["ResID"]
	    }  
)

expect("releaseReservation2", 
        lambda x: x["result"] == {}, API, "releaseReservation",
       {
			"ResID": r2["result"]["ResID"]
	    }  
)

