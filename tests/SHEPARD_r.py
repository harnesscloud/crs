#!/usr/bin/env python
from trest import expect

API="http://localhost:7075"


expect("releaseAllResources",
       lambda x: x["result"] == {}, API, "releaseAllResources")

av=expect("getAvailableResources", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Quantity"] == "8", API, "getAvailableResources")

r1=expect("reserveDFE-1",
        lambda x: len(x["result"]["Reservations"]) == 1, API, "reserveResources",
       {
			"Resources":[
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":1
						}
				  }
		   ]
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
exit(0)
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

print "All tests passed!"
