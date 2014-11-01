#!/usr/bin/env python
from trest import expect

API="http://localhost:8080"
       
expect("getResourceTypes", 
       lambda x: ("result" in x) and ("Types" in x["result"]) and (x["result"]["Types"][0]["Type"] == "Storage"), 
       API, "getResourceTypes")


expect("calculateResourceCapacity_simple_reserve",
       lambda x: False, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"Storage",
						"Attributes":{
						   "Capacity":10,
						   "Throughput":100,
						   "AccessType":"SEQUENTIAL"
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Capacity": 3, "Throughput":0,"AccessType":"SEQUENTIAL" } } ],
  	      "Release": []
  	    }
)	  


expect("calculateResourceCapacity_multiple_reserves",
       lambda x: x["result"]["Attributes"]["Quantity"]==5, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Quantity": 3 } },
    	        { "Attributes": { "Quantity": 1 } },
    	        { "Attributes": { "Quantity": 1 } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_to_zero",
       lambda x: x["result"]["Attributes"]["Quantity"]==0, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Quantity": 3 } },
    	        { "Attributes": { "Quantity": 1 } },
    	        { "Attributes": { "Quantity": 6 } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_releases",
       lambda x: x["result"]["Attributes"]["Quantity"]==20, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  },
  	      "Release":
  	         [ { "Attributes": { "Quantity": 3 } },
    	        { "Attributes": { "Quantity": 1 } },
    	        { "Attributes": { "Quantity": 6 } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_exceed_capacity",
       lambda x: x["result"] == {}, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Quantity": 3 } },
    	        { "Attributes": { "Quantity": 1 } },
    	        { "Attributes": { "Quantity": 7 } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_releases_border",
       lambda x: x["result"]["Attributes"]["Quantity"]==0, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Quantity": 3 } },
    	        { "Attributes": { "Quantity": 1 } },
    	        { "Attributes": { "Quantity": 7 } }    	       
  	         ],
  	      "Release":
  	         [ { "Attributes": { "Quantity": 1 } },
    	        { "Attributes": { "Quantity": 0 } },
    	        { "Attributes": { "Quantity": 0 } }    	       
  	         ]  	         
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_releases_with_5_left",
       lambda x: x["result"]["Attributes"]["Quantity"]==5, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Quantity": 3 } },
    	        { "Attributes": { "Quantity": 1 } },
    	        { "Attributes": { "Quantity": 7 } }    	       
  	         ],
  	      "Release":
  	         [ { "Attributes": { "Quantity": 1 } },
    	        { "Attributes": { "Quantity": 2 } },
    	        { "Attributes": { "Quantity": 3 } }    	       
  	         ]  	         
  	    }
)	

expect("calculateResourceAgg_single",
       lambda x: x["result"]["Attributes"]["Capacity"]==10, API, "calculateResourceAgg",
       {
			"Resources": [
				  {
						"Type":"Storage",
						"Attributes":{
						   "Capacity":10,
						   "Throughput": 10,
						   "AccessType": "SEQUENTIAL"
						}
				  }				  
	      ]
	         
  	    }
)

expect("calculateResourceAgg_multi",
       lambda x: (x["result"]["Attributes"]["Capacity"]==23) and (x["result"]["Attributes"]["Throughput"]==15), API, "calculateResourceAgg",
       {
			"Resources": [
				  {
						"Type":"Storage",
						"Attributes":{
						   "Capacity":10,
						   "Throughput": 15,
						   "AccessType": "SEQUENTIAL"						   
						}
				  },
				  {
						"Type":"Storage",
						"Attributes":{
						   "Capacity":13,
						   "Throughput": 10,
						   "AccessType": "SEQUENTIAL"						   
						}
				  }
				  
	      ]
	         
  	    }
)	

print "All tests passed!"

