#!/usr/bin/env python
from trest import expect
from trest import p

API="http://192.168.1.6:8888"
 

r=expect("getAvailableResources", 
        lambda x: len(x["result"]["Resources"])>=1, API, "getAvailableResources")

      
r1=expect("reserveVM-1",
        lambda x: len(x["result"]["Reservations"]) == 1, API, "reserveResources",
       {
          "Resources":[
          {
             "Type":"Machine",
             "ID":r["result"]["Resources"][0]["ID"],
             "IP":r["result"]["Resources"][0]["IP"],
             "Attributes":
                 { "Cores": 2,
                   "Memory": 200,
                   "Disk": 10
                 }
                 
          }
          ]
	    }  
)	

r1=expect("reserveVM-2",
        lambda x: len(x["result"]["Reservations"]) == 1, API, "reserveResources",
       {
          "Resources":[
          {
             "Type":"Machine",
             "ID":r["result"]["Resources"][0]["ID"],
             "IP":r["result"]["Resources"][0]["IP"],
             "Attributes":
                 { "Cores": 25,
                   "Memory": 200,
                   "Disk": 1000
                 }
                 
          }
          ]
	    }  
)	


expect("verifyResources-1",
        lambda x: x["result"]["Reservations"][0]["Ready"], API, "verifyResources",
       {
         "Reservations": r1["result"]["Reservations"]
	    }  
)	


expect("verifyResources-2",
        lambda x: x["result"]["Reservations"][0]["Ready"], API, "verifyResources",
       {
         "Reservations": r1["result"]["Reservations"]
	    }  
)	


print r1["result"]["Reservations"]
expect("releaseVM-1",
        lambda x: x["result"] == {}, API, "releaseResources",
       {
          "Reservations": r1["result"]["Reservations"]
	    }  
)	


print "All tests passed!"
