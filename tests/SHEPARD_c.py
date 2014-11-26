#!/usr/bin/env python
from trest import expect

API="http://localhost:7075"
       
expect("getResourceTypes", 
       lambda x: ("result" in x) and ("Types" in x["result"]) and (x["result"]["Types"][0]["Type"] == "DFECluster"), 
       API, "getResourceTypes")

expect("calculateResourceCapacity_simple_reserve",
       lambda x: (x["result"]["Resource"]["Attributes"]["Size"]==7) and (x["result"]["Resource"]["Type"] == "DFECluster"), API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Size": 3 } } ]
  	    }
)	  


expect("calculateResourceCapacity_multiple_reserves",
       lambda x: x["result"]["Resource"]["Attributes"]["Size"]==5, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Size": 3 } },
    	        { "Attributes": { "Size": 1 } },
    	        { "Attributes": { "Size": 1 } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_to_zero",
       lambda x: x["result"]["Resource"]["Attributes"]["Size"]==0, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Size": 3 } },
    	        { "Attributes": { "Size": 1 } },
    	        { "Attributes": { "Size": 6 } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_releases",
       lambda x: x["result"]["Resource"]["Attributes"]["Size"]==20, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":10
						}
				  },
  	      "Release":
  	         [ { "Attributes": { "Size": 3 } },
    	        { "Attributes": { "Size": 1 } },
    	        { "Attributes": { "Size": 6 } }    	       
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
						   "Size":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Size": 3 } },
    	        { "Attributes": { "Size": 1 } },
    	        { "Attributes": { "Size": 7 } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_releases_border",
       lambda x: x["result"]["Resource"]["Attributes"]["Size"]==0, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Size": 3 } },
    	        { "Attributes": { "Size": 1 } },
    	        { "Attributes": { "Size": 7 } }    	       
  	         ],
  	      "Release":
  	         [ { "Attributes": { "Size": 1 } },
    	        { "Attributes": { "Size": 0 } },
    	        { "Attributes": { "Size": 0 } }    	       
  	         ]  	         
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_releases_with_5_left",
       lambda x: x["result"]["Resource"]["Attributes"]["Size"]==5, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":10
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Size": 3 } },
    	        { "Attributes": { "Size": 1 } },
    	        { "Attributes": { "Size": 7 } }    	       
  	         ],
  	      "Release":
  	         [ { "Attributes": { "Size": 1 } },
    	        { "Attributes": { "Size": 2 } },
    	        { "Attributes": { "Size": 3 } }    	       
  	         ]  	         
  	    }
)	

expect("calculateResourceAgg_single",
       lambda x: x["result"]["Attributes"]["Size"] == 10, API, "calculateResourceAgg",
       {
			"Resources": [
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":10
						}
				  }
	      ]
	         
  	    }
)

expect("calculateResourceAgg_multi",
       lambda x: x["result"]["Attributes"]["Size"] == 23, API, "calculateResourceAgg",
       {
			"Resources": [
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":10
						}
				  },
				  {
						"Type":"DFECluster",
						"Attributes":{
						   "Size":13
						}
				  }
				  
	      ]
	         
  	    }
)	

print "All tests passed!"

