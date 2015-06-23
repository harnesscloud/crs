#!/usr/bin/env python
from trest import expect

API="http://localhost:5558"
   
expect("releaseAllReservations", 
       lambda x: x["result"] == {}, 
       API, "releaseAllReservations")
             
expect("getResourceTypes", 
       lambda x: ("result" in x) and ("Types" in x["result"]) and len(x["result"]["Types"]) == 2, 
       API, "getResourceTypes")


####################################################### prepareReservation
p1=expect("prepRes1", 
        lambda x: len(x["result"]["Resources"]) == 5, API, "prepareReservation",
       {
         "Resources":[
          {
  	          "GroupID": "G0",          
             "Type":"Machine",
             "NumInstances": 4,
             "Attributes":
                 { "Cores": 3,
                   "Memory": 200,
                   "Disk": 8
                 }
          },
				  {
				      "GroupID": "G1",
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":2
						}
				  }          
          
          
          ]
	    }  
) 

r1 = expect("createReservation1", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p1["result"]["ConfigID"]
	    }  
)

exit(0)
p2=expect("prepRes2", 
        lambda x: len(x["result"]["Resources"]) == 1, API, "prepareReservation",
       {
          "Resources":[
          {
  	          "GroupID": "G0",          
             "Type":"Machine",
             "NumInstances": 1,
             "Attributes":
                 { "Cores": 12,
                   "Memory": 200,
                   "Disk": 8
                 }
          }
          ]
	    }  
) 

r2 = expect("createReservation2", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p2["result"]["ConfigID"]
	    }  
)



p3=expect("prepRes3", 
        lambda x: len(x["result"]["Resources"]) == 4, API, "prepareReservation",
       {
          "Resources":[
          {
  	          "GroupID": "G0",          
             "Type":"Machine",
             "NumInstances": 4,
             "Attributes":
                 { "Cores": 3,
                   "Memory": 200,
                   "Disk": 8
                 }
          }
          ]
	    }  
) 

r3 = expect("createReservation3", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p3["result"]["ConfigID"]
	    }  
)

expect("releaseReservation2", 
        lambda x: x["result"]=={}, API, "releaseReservation",
       {
			"ResID": r2["result"]["ResID"]
	    }  
)

expect("releaseReservation3", 
        lambda x: x["result"]=={}, API, "releaseReservation",
       {
			"ResID": r3["result"]["ResID"]
	    }  
)

exit(0)
r1 = expect("createReservation1", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p1["result"]["ConfigID"]
	    }  
)

r2=expect("checkReservation1", 
        lambda x: x["result"]["Ready"], API, "checkReservation",
       {
			"ResID": r1["result"]["ResID"]
	    }  
)


print "address for r1: ", r2["result"]["Addresses"]

expect("releaseReservation1", 
        lambda x: x["result"]=={}, API, "releaseReservation",
       {
			"ResID": r1["result"]["ResID"]
	    }  
)

'''
expect("getSimpleMachineReq2", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Cores"] == 16, API, "prepareReservation",
       {
          "Resources":[
          {
  	          "GroupID": "ID0",          
             "Type":"Machine",
             "Attributes":
                 { "Cores": 16,
                   "Memory": 200,
                   "Disk": 10
                 }
                 
          }
          ]
	    }  
) 
expect("getSimpleMachineReq2_expect_fail1", 
        lambda x: x["result"] == {}, API, "prepareReservation",
       {
          "Resources":[
          {
  	          "GroupID": "ID0",          
             "Type":"Machine",
             "Attributes":
                 { "Cores": 17,
                   "Memory": 200,
                   "Disk": 10
                 }
                 
          }
          ]
	    }  
) 

expect("getSimpleMachineReq2_expect_fail2", 
        lambda x: x["result"] == {}, API, "prepareReservation",
       {
          "Resources":[
          {
  	          "GroupID": "ID0",          
             "Type":"Machine",
             "Attributes":
                 { "Cores": 16,
                   "Memory": 10694,
                   "Disk": 10
                 }
                 
          }
          ]
	    }  
) 


expect("getSimpleMachineReq3", 
        lambda x: len(x["result"]["Resources"]) == 3 and (x["result"]["Resources"][0]["Attributes"]["Cores"] == 2), 
               API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Machine",
						"NumInstances":3,
						"Attributes":
				        { "Cores": 2,
		                "Memory": 200,
		                "Disk": 10
		              }
				  }
		   ]
	    }  
) 

expect("getSimpleMachineReq4", 
        lambda x: len(x["result"]["Resources"]) == 5 and (x["result"]["Resources"][0]["Attributes"]["Cores"] == 2), 
               API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Machine",
						"NumInstances":3,
						"Attributes":
				        { "Cores": 2,
		                "Memory": 200,
		                "Disk": 10
		              }
				  },
			  {
				      "GroupID": "ID1",
						"Type":"Machine",
						"NumInstances":2,
						"Attributes":
				        { "Cores": 4,
		                "Memory": 200,
		                "Disk": 10
		              }
				  }				  
		   ]
	    }  
) 

expect("getSimpleMachineReq_expect_fail_cores1", 
        lambda x: x["result"] == {}, 
               API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Machine",
						"NumInstances":17,
						"Attributes":
				        { "Cores": 2,
		                "Memory": 50,
		                "Disk": 5
		              }
				  }				  
		   ]
	    }  
) 

expect("getSimpleMachineReq_bound0", 
        lambda x: len(x["result"]["Resources"]) == 4, 
               API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Machine",
						"NumInstances":4,
						"Attributes":
				        { "Cores": 4,
		                "Memory": 50,
		                "Disk": 5
		              }
				  }				  
		   ]
	    }  
)

expect("getSimpleMachineReq_bound1", 
        lambda x: len(x["result"]["Resources"]) == 8, 
               API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Machine",
						"NumInstances":8,
						"Attributes":
				        { "Cores": 4,
		                "Memory": 50,
		                "Disk": 5
		              }
				  }				  
		   ]
	    }  
) 
 
expect("getSimpleMachineReq_bound2", 
        lambda x: x["result"]=={}, 
               API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Machine",
						"NumInstances":9,
						"Attributes":
				        { "Cores": 4,
		                "Memory": 50,
		                "Disk": 5
		              }
				  }				  
		   ]
	    }  
)  

p0=expect("getSimpleMachineReq5", 
        lambda x: len(x["result"]["Resources"]) == 4, 
               API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"Machine",
						"NumInstances":4,
						"Attributes":
				        { "Cores": 5,
		                "Memory": 50,
		                "Disk": 5
		              }
				  }				  
		   ]
	    }  
) 

r0 = expect("createReservation1", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p0["result"]["ConfigID"]
	    }  
)

expect("checkReservation2", 
        lambda x: x["result"]["Ready"], API, "checkReservation",
       {
			"ResID": r0["result"]["ResID"]
	    }  
)

expect("releaseReservation2", 
        lambda x: x["result"]=={}, API, "releaseReservation",
       {
			"ResID": r0["result"]["ResID"]
	    }  
)
'''
print "All tests passed!"


