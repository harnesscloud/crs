#!/usr/bin/env python
from trest import expect
import json
  
API="http://localhost:8888"

print "Using API: " + API
     
r=expect("getAvailableResources", 
        lambda x: len(x["result"]["Resources"])>=1, API, "getAvailableResources")

print "AVAILABLE RESOURCES: ", r

expect("calculateResourceCapacity1",
        lambda x: x["result"]["Resource"]["Attributes"]["Cores"]==7, API, "calculateResourceCapacity",
       {
          "Resource":
          {
             "Type":"Machine",
             "Attributes":
                 { "Cores": 10,
                   "Memory": 200,
                   "Disk": 10,
                   "Frequency": 2500
                 }
                 
          },
          "Reserve":
             [ 
               {
                  "Attributes":
		              { "Cores": 3,
		                "Memory": 200,
		                "Disk": 10,
                      "Frequency": 2500		                
  		              }
               }
             ]          
	    }  
)	

expect("calculateResourceCapacity2",
        lambda x: x["result"]["Resource"]["Attributes"]["Cores"]==0, API, "calculateResourceCapacity",
       {
          "Resource":
          {
             "Type":"Machine",
             "Attributes":
                 { "Cores": 10,
                   "Memory": 200,
                   "Disk": 10,
                   "Frequency": 2500
                 }
                 
          },
          "Reserve":
             [ 
               {
                  "Attributes":
		              { "Cores": 10,
		                "Memory": 200,
		                "Disk": 10,
                      "Frequency": 2500		                
  		              }
               }
             ]          
	    }  
)	
expect("calculateResourceCapacity3",
        lambda x: x["result"]=={}, API, "calculateResourceCapacity",
       {
          "Resource":
          {
             "Type":"Machine",
             "Attributes":
                 { "Cores": 10,
                   "Memory": 200,
                   "Disk": 10,
                   "Frequency": 2500
                 }
                 
          },
          "Reserve":
             [ 
               {
                  "Attributes":
		              { "Cores": 11,
		                "Memory": 200,
		                "Disk": 10,
                      "Frequency": 2500		                
  		              }
               }
             ]          
	    }  
)	
expect("calculateResourceCapacity3",
        lambda x: x["result"]=={}, API, "calculateResourceCapacity",
       {
          "Resource":
          {
             "Type":"Machine",
             "Attributes":
                 { "Cores": 11,
                   "Memory": 201,
                   "Disk": 10,
                   "Frequency": 2500
                 }
                 
          },
          "Reserve":
             [ 
               {
                  "Attributes":
		              { "Cores": 11,
		                "Memory": 202,
		                "Disk": 10,
                      "Frequency": 2500		                
  		              }
               }
             ]          
	    }  
)

expect("calculateResourceCapacity4",
        lambda x: x["result"]["Resource"]["Attributes"]["Cores"]==11, API, "calculateResourceCapacity",
       {
          "Resource":
          {
             "Type":"Machine",
             "Attributes":
                 { "Cores": 11,
                   "Memory": 201,
                   "Disk": 10,
                   "Frequency": 2500
                 }
                 
          },
          "Reserve":
             [ 
               {
                  "Attributes":
		              { "Cores": 11,
		                "Memory": 202,
		                "Disk": 10,
                      "Frequency": 2500		                
  		              }
               },
               {
                  "Attributes":
		              { "Cores": 11,
		                "Memory": 202,
		                "Disk": 10,
                      "Frequency": 2500		                
  		              }
  		         }
             ],
          "Release":
             [ 
               {
                  "Attributes":
		              { "Cores": 11,
		                "Memory": 202,
		                "Disk": 10,
                      "Frequency": 2500		                
  		              }
               },
               {
                  "Attributes":
		              { "Cores": 11,
		                "Memory": 202,
		                "Disk": 10,
                      "Frequency": 2500		                
  		              }
  		          }
             ]
                       
	    }  
)

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

r2=expect("reserveVM-2",
        lambda x: len(x["result"]["Reservations"]) == 3, API, "reserveResources",
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
                 
          },
          {
             "Type":"Machine",
             "ID":r["result"]["Resources"][0]["ID"],
             "IP":r["result"]["Resources"][0]["IP"],
             "Attributes":
                 { "Cores": 3,
                   "Memory": 200,
                   "Disk": 10
                 }
                 
          },          
          {
             "Type":"Machine",
             "ID":r["result"]["Resources"][0]["ID"],
             "IP":r["result"]["Resources"][0]["IP"],
             "Attributes":
                 { "Cores": 4,
                   "Memory": 200,
                   "Disk": 10
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
         "Reservations": r2["result"]["Reservations"]
	    }  
)	


expect("releaseVM-1",
        lambda x: x["result"] == {}, API, "releaseResources",
       {
          "Reservations": r1["result"]["Reservations"]
	    }  
)	


expect("releaseVM-2",
        lambda x: x["result"] == {}, API, "releaseResources",
       {
          "Reservations": r2["result"]["Reservations"]
	    }  
)	




print "All tests passed!"
