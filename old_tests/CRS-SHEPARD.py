#!/usr/bin/env python
from trest import expect

API="http://localhost:56789"

       
expect("getResourceTypes", 
       lambda x: ("result" in x) and ("Types" in x["result"]) and (x["result"]["Types"][0]["Type"] == "DFECluster"), 
       API, "getResourceTypes")

####################################################### prepareReservation
p1 = expect("getSimpleDFEReq1", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Size"] == 1, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"DFECluster",
						"NumInstances":1,
						"Attributes":{
						   "Size":1
						}
				  }
		   ],
		   "Distances":[]
	    }  
) 

p2 = expect("getSimpleDFEReq2", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Size"] == 4, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"DFECluster",
						"NumInstances":1,
						"Attributes":{
						   "Size":4
						}
				  }
		   ],
		   "Distances":[]
	    }  
) 

p3 = expect("getSimpleDFEReq3", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Size"] == 3, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",
						"Type":"DFECluster",
						"NumInstances":1,
						"Attributes":{
						   "Size":3
						}
				  }
		   ],
		   "Distances":[]
	    }  
) 


expect("getSimpleDFEReq4", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Size"] == 4, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",				  
						"Type":"DFECluster",
						"NumInstances":2,
						"Attributes":{
						   "Size":4
						}
				  }
		   ]
	    }  
) 

expect("getSimpleDFEReq8", 
        lambda x: x["result"]["Resources"][0]["Attributes"]["Size"] == 8, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",						  
						"Type":"DFECluster",
						"NumInstances":1,
						"Attributes":{
						   "Size":8
						}
				  }
		   ]
	    }  
) 

expect("getSimpleDFEReq9_expect_fail", 
        lambda x: x["result"] == { }, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",						  
						"Type":"DFECluster",
						"NumInstances":1,
						"Attributes":{
						   "Size":9
						}
				  }
		   ]
	    }  
) 

expect("getSimpleDFEReq_multiple_instances1", 
        lambda x: ("ConfigID" in x["result"]) and (len(x["result"]["Resources"]) == 2) and x["result"]["Resources"][0]["Attributes"]["Size"] ==1, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",						  
						"Type":"DFECluster",
						"NumInstances":2,
						"Attributes":{
						   "Size":1
						}
				  }
		   ]
	    }  
) 

expect("getSimpleDFEReq_multiple_instances2", 
        lambda x: ("ConfigID" in x["result"]) and (len(x["result"]["Resources"]) == 2) and x["result"]["Resources"][0]["Attributes"]["Size"] == 4, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",						  
						"Type":"DFECluster",
						"NumInstances":2,
						"Attributes":{
						   "Size":4
						}
				  }
		   ]
	    }  
) 

expect("getSimpleDFEReq_multiple_instances3_expect_fail", 
        lambda x: x["result"] == { }, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",						  
						"Type":"DFECluster",
						"NumInstances":3,
						"Attributes":{
						   "Size":4
						}
				  }
		   ]
	    }  
) 

expect("getMultipleDFEReq1", 
        lambda x: ("ConfigID" in x["result"]) and (len(x["result"]["Resources"]) == 2) and x["result"]["Resources"][0]["Attributes"]["Size"] == 2, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",						  
						"Type":"DFECluster",
						"NumInstances":1,
						"Attributes":{
						   "Size":2
						}
				  },
				  {
				      "GroupID": "ID1",						  
						"Type":"DFECluster",
						"NumInstances":1,
						"Attributes":{
						   "Size":3
						}
				  }
				  
		   ]
	    }  
) 

expect("getMultipleDFEReq_multiple_instances1", 
        lambda x: ("ConfigID" in x["result"]) and (len(x["result"]["Resources"]) == 5) and x["result"]["Resources"][0]["Attributes"]["Size"] == 2, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",						  
						"Type":"DFECluster",
						"NumInstances":2,
						"Attributes":{
						   "Size":2
						}
				  },
				  {
				      "GroupID": "ID1",						  
						"Type":"DFECluster",
						"NumInstances":3,
						"Attributes":{
						   "Size":1
						}
				  }
				  
		   ]
	    }  
) 

expect("getMultipleDFEReq_multiple_instances2", 
        lambda x: ("ConfigID" in x["result"]) and (len(x["result"]["Resources"]) == 5) and x["result"]["Resources"][0]["Attributes"]["Size"] == 2, API, "prepareReservation",
       {
			"Resources":[
				  {
				      "GroupID": "ID0",						  
						"Type":"DFECluster",
						"NumInstances":2,
						"Attributes":{
						   "Size":2
						}
				  },
				  {
				      "GroupID": "ID1",						  
						"Type":"DFECluster",
						"NumInstances":3,
						"Attributes":{
						   "Size":1
						}
				  }
				  
		   ]
	    }  
) 

####################################################### createReservation/releaseReservation
r1 = expect("createReservation1", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p1["result"]["ConfigID"]
	    }  
)

expect("checkReservation1", 
        lambda x: x["result"]["Ready"], API, "checkReservation",
       {
			"ResID": r1["result"]["ResID"]
	    }  
)


expect("releaseReservation1", 
        lambda x: x["result"] == {}, API, "releaseReservation",
       {
			"ResID": r1["result"]["ResID"]
	    }  
)


r2 = expect("createReservation2", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p2["result"]["ConfigID"]
	    }  
)  


expect("checkReservation2", 
        lambda x: x["result"]["Ready"], API, "checkReservation",
       {
			"ResID": r2["result"]["ResID"]
	    }  
)

expect("releaseReservation2", 
        lambda x: x["result"] == {}, API, "releaseReservation",
       {
			"ResID": r2["result"]["ResID"]
	    }  
)

r3=expect("createReservation3", 
        lambda x: "ResID" in x["result"], API, "createReservation",
       {
			"ConfigID": p3["result"]["ConfigID"]
	    }  
)  


expect("checkReservation3", 
        lambda x: x["result"]["Ready"], API, "checkReservation",
       {
			"ResID": r3["result"]["ResID"]
	    }  
)


expect("releaseReservation3", 
        lambda x: x["result"] == {}, API, "releaseReservation",
       {
			"ResID": r3["result"]["ResID"]
	    }  
)

