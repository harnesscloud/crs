#!/usr/bin/env python
from trest import expect

API="http://localhost:8080"
       
expect("getResourceTypes", 
       lambda x: ("result" in x) and ("Types" in x["result"]) and (x["result"]["Types"][0]["Type"] == "Storage"), 
       API, "getResourceTypes")


expect("calculateResourceCapacity_simple_reserve_capacity",
       lambda x: x["result"]["Resource"]["Attributes"]["Capacity"] == 7, API, "calculateResourceCapacity",
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

expect("calculateResourceCapacity_mixed_reserve_capacity",
       lambda x: x["result"] == {}, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"Storage",
						"Attributes":{
						   "Capacity":10,
						   "Throughput":100,
						   "AccessType":"RANDOM"
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Capacity": 3, "Throughput":0,"AccessType":"SEQUENTIAL" } } ],
  	      "Release": []
  	    }
)	

expect("calculateResourceCapacity_simple_reserve_throughput",
       lambda x: x["result"]["Resource"]["Attributes"]["Throughput"] == 80, API, "calculateResourceCapacity",
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
  	         [ { "Attributes": { "Capacity": 3, "Throughput":20,"AccessType":"SEQUENTIAL" } } ],
  	      "Release": []
  	    }
)	  



expect("calculateResourceCapacity_multiple_reserves_capacity",
       lambda x: x["result"]["Resource"]["Attributes"]["Capacity"] == 5, API, "calculateResourceCapacity",
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
  	         [ { "Attributes": { "Capacity": 3,"AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 1,"AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 1,"AccessType":"SEQUENTIAL" } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_throughput",
       lambda x: (x["result"]["Resource"]["Attributes"]["Throughput"] == 50) and (x["result"]["Resource"]["Attributes"]["Capacity"] == 10), API, "calculateResourceCapacity",
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
  	         [ { "Attributes": { "Throughput": 30,"AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Throughput": 10,"AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Throughput": 10,"AccessType":"SEQUENTIAL" } }    	       
  	         ]
  	    }
)	

## error: should return Capacity == 0 ##

expect("calculateResourceCapacity_multiple_reserves_to_zero_capacity",
       lambda x:  x["result"]["Resource"]["Attributes"]["Capacity"] == 0, API, "calculateResourceCapacity",
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
  	         [ { "Attributes": { "Capacity": 3, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 1, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 6, "AccessType":"SEQUENTIAL" } }    	       
  	         ]
  	    }
)	


## error: should return Throughput == 0 ##

expect("calculateResourceCapacity_multiple_reserves_to_zero_throughput",
       lambda x:  x["result"]["Resource"]["Attributes"]["Throughput"] == 0, API, "calculateResourceCapacity",
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
  	         [ { "Attributes": { "Throughput": 30, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Throughput": 10, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Throughput": 60, "AccessType":"SEQUENTIAL" } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_releases",
       lambda x: x["result"]["Resource"]["Attributes"]["Capacity"] == 20, API, "calculateResourceCapacity",
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
  	      "Release":
  	         [ { "Attributes": { "Capacity": 3, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 1, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 6, "AccessType":"SEQUENTIAL" } }    	       
  	         ]
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_exceed_capacity",
       lambda x: x["result"] == {}, API, "calculateResourceCapacity",
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
  	         [ { "Attributes": { "Capacity": 3, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 1, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 7, "AccessType":"SEQUENTIAL" } }    	       
  	         ]
  	    }
)	


expect("calculateResourceCapacity_multiple_reserves_releases_border",
       lambda x: x["result"]["Resource"]["Attributes"]["Capacity"] == 0, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"Storage",
						"Attributes":{
						   "Capacity":10,
   					   "Throughput":100,
						   "AccessType":"RANDOM"						   
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Capacity": 3, "AccessType":"RANDOM" } },
    	        { "Attributes": { "Capacity": 1, "AccessType":"RANDOM" } },
    	        { "Attributes": { "Capacity": 7, "AccessType":"RANDOM" } }    	       
  	         ],
  	      "Release":
  	         [ { "Attributes": { "Capacity": 1, "AccessType":"RANDOM"  } },
    	        { "Attributes": { "Capacity": 0, "AccessType":"RANDOM"  } },
    	        { "Attributes": { "Capacity": 0, "AccessType":"RANDOM"  } }    	       
  	         ]  	         
  	    }
)	


expect("calculateResourceCapacity_multiple_reserves_releases_border_mix",
       lambda x: x["result"] == {}, API, "calculateResourceCapacity",
       {
			"Resource":
				  {
						"Type":"Storage",
						"Attributes":{
						   "Capacity":10,
   					   "Throughput":100,
						   "AccessType":"RANDOM"						   
						}
				  },
  	      "Reserve":
  	         [ { "Attributes": { "Capacity": 3, "AccessType":"RANDOM" } },
    	        { "Attributes": { "Capacity": 1, "AccessType":"RANDOM" } },
    	        { "Attributes": { "Capacity": 7, "AccessType":"RANDOM" } }    	       
  	         ],
  	      "Release":
  	         [ { "Attributes": { "Capacity": 1, "AccessType":"SEQUENTIAL"  } },
    	        { "Attributes": { "Capacity": 0, "AccessType":"SEQUENTIAL"  } },
    	        { "Attributes": { "Capacity": 0, "AccessType":"SEQUENTIAL"  } }    	       
  	         ]  	         
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_releases_with_5_left_capacity",
       lambda x: x["result"]["Resource"]["Attributes"]["Capacity"]==5, API, "calculateResourceCapacity",
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
  	         [ { "Attributes": { "Capacity": 3, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 1, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 7, "AccessType":"SEQUENTIAL" } }    	       
  	         ],
  	      "Release":
  	         [ { "Attributes": { "Capacity": 1, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 2, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Capacity": 3, "AccessType":"SEQUENTIAL" } }    	       
  	         ]  	         
  	    }
)	

expect("calculateResourceCapacity_multiple_reserves_releases_with_5_left_throughput",
       lambda x: x["result"]["Resource"]["Attributes"]["Throughput"]==50, API, "calculateResourceCapacity",
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
  	         [ { "Attributes": { "Throughput": 30, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Throughput": 10, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Throughput": 70, "AccessType":"SEQUENTIAL" } }    	       
  	         ],
  	      "Release":
  	         [ { "Attributes": { "Throughput": 10, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Throughput": 20, "AccessType":"SEQUENTIAL" } },
    	        { "Attributes": { "Throughput": 30, "AccessType":"SEQUENTIAL" } }    	       
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

