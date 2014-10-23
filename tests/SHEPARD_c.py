#!/usr/bin/env python
from trest import expect

API="http://localhost:7075"
       
expect("getResourceTypes", 
       lambda x: ("result" in x) and ("Types" in x["result"]) and (x["result"]["Types"][0]["Type"] == "DFECluster"), 
       API, "getResourceTypes")

expect("calculateResourceCapacity_simple_reserve",
       lambda x: x["result"]["Attributes"]["Quantity"]==7, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Quantity": 3 } } ]
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
       lambda x: x["result"]["Attributes"]["Quantity"] == 10, API, "calculateResourceAgg",
       {
			"Resources": [
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  }
	      ]
	         
  	    }
)

expect("calculateResourceAgg_multi",
       lambda x: x["result"]["Attributes"]["Quantity"] == 23, API, "calculateResourceAgg",
       {
			"Resources": [
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":10
						}
				  },
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Quantity":13
						}
				  }
				  
	      ]
	         
  	    }
)	

print "All tests passed!"

