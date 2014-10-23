#!/usr/bin/env python
from trest import expect

API="http://localhost:5558"
      
expect("getResourceTypes", 
       lambda x: ("result" in x) and ("Types" in x["result"]) and (x["result"]["Types"][0]["Type"] == "Machine"), 
       API, "getResourceTypes")


####################################################### prepareReservation
expect("getSimpleMachineReq1", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Cores"] == 2, API, "prepareReservation",
       {
          "Resources":[
          {
  	          "GroupID": "ID0",          
             "Type":"Machine",
             "Attributes":
                 { "Cores": 2,
                   "Memory": 200,
                   "Disk": 10,
                   "Frequency": 2400
                 }
                 
          }
          ]
	    }  
) 

expect("getSimpleMachineReq2", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Cores"] == 10, API, "prepareReservation",
       {
          "Resources":[
          {
  	          "GroupID": "ID0",          
             "Type":"Machine",
             "Attributes":
                 { "Cores": 10,
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
				        { "Cores": 3,
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
				        { "Cores": 3,
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

print "All tests passed!"


