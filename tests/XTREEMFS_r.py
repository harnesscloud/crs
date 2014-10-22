#!/usr/bin/env python
from trest import expect

API="http://localhost:8080"

'''      
expect("releaseAllResources",
       lambda x: x["result"] == {}, API, "releaseAllResources", { })
 
'''
expect("getAvailableResources", 
        lambda x: len(x["result"]["Resources"]) == 2, API, "getAvailableResources")


r1=expect("reserveStorage-1",
        lambda x: len(x["result"]["Reservations"]) == 1, API, "reserveResources",
       {
			"Resources":[
				  {
						"Type":"Storage",
						"Attributes":{
			            "Capacity":10,
						   "Throughput": 15,
						   "AccessType": "SEQUENTIAL"	
						}
				  }
		   ]
	    }  
)	
print "reservation...", r1["result"]
expect("checkReserveStorage-1",
        lambda x: x["result"]["Reservations"][0]["Ready"], API, "verifyResources",
       {
			"Reservations":r1["result"]["Reservations"]			
	    }  
)	
'''        
expect("releaseReserveStorage-1",
        lambda x: x["result"] == { }, API, "releaseResources",
       {
			"Reservations":r1["result"]["Reservations"]			
	    }  
)	 


r2=expect("reserveDFE-5",
        lambda x: len(x["result"]["Reservations"]) == 1, API, "reserveResources",
       {
			"Resources":[
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":5
						}
				  }
		   ]
	    }  
)	            

expect("reserveDFE-3_to_fail",
        lambda x: ("error" in x) and (x["error"]["message"].find("Insufficient resources") != -1), API, "reserveResources",
       {
			"Resources":[
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":3
						}
				  }
		   ]
	    }  
)	

expect("checkReserveDFE-1",
        lambda x: x["result"]["Reservations"][0]["Ready"], API, "verifyResources",
       {
			"Reservations":r1["result"]["Reservations"]			
	    }  
)	    

expect("checkReserveDFE-5",
        lambda x: x["result"]["Reservations"][0]["Ready"], API, "verifyResources",
       {
			"Reservations":r2["result"]["Reservations"]			
	    }  
)	    

expect("releaseReserveDFE-1",
        lambda x: x["result"] == { }, API, "releaseResources",
       {
			"Reservations":r1["result"]["Reservations"]			
	    }  
)	    

expect("releaseReserveDFE-5",
        lambda x: x["result"] == { }, API, "releaseResources",
       {
			"Reservations":r2["result"]["Reservations"]			
	    }  
)	    
'''
print "All tests passed!"
