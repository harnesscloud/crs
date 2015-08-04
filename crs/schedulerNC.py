import deps
import copy
import sys, traceback
from hresman import utils

from glpk import *
from glpk.glpk_parser import *
from glpk.glpkpi import *

'''   
Managers: {'1d1c5582-1b74-11e5-bba3-60a44cabf185': {'Name': u'IRM-SEAL\n', 'ManagerID': '1d1c5582-1b74-11e5-bba3-60a44cabf185', 'Port': 54106, 'Address': '127.0.0.1'}, '1e2e967e-1b74-11e5-bba3-60a44cabf185': {'Name': u'IRM-HERON\n', 'ManagerID': '1e2e967e-1b74-11e5-bba3-60a44cabf185', 'Port': 51186, 'Address': '127.0.0.1'}}

Resources: {'1d1c5582-1b74-11e5-bba3-60a44cabf185': {u'ID2': {u'Attributes': {u'a': 9, u'c': 5, u'b': 4}, u'Type': u'Device'}, u'ID3': {u'Attributes': {u'a': 2, u'c': 8, u'b': 10}, u'Type': u'Device'}, u'ID1': {u'Attributes': {u'a': 2, u'c': 5, u'b': 3}, u'Type': u'Device'}}, '1e2e967e-1b74-11e5-bba3-60a44cabf185': {u'ID2': {u'Attributes': {u'a': 4, u'c': 2, u'b': 8}, u'Type': u'Device'}, u'ID3': {u'Attributes': {u'a': 2, u'c': 7, u'b': 3}, u'Type': u'Device'}, u'ID1': {u'Attributes': {u'a': 2, u'c': 3, u'b': 5}, u'Type': u'Device'}}}

Allocations: [{u'Group': u'g0', u'Type': u'Machine', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g0', u'Type': u'Machine', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g0', u'Type': u'DFECluster', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}]
    '''
class Resource:
    def __init__(self, idx):
        self.id = idx
        self.key = None
        self.attributes = { }
        self.irm = None
        self.type = None
        self.group = None
        self.source = None
        self.target = None

class Constraint:
    def __init__(self, idx):
        self.id = idx
        self.key = None
        self.opoeration = None
        self.addends = [ ]
        self.threshold = None


   
def generate_lp(filename, resources, compound_resources, constraints, reservation, compound_reservation, distances, compound_attributes, distance_attributes) :
  
  reservation_size = len(reservation)
  num_resources = len(resources)
  
  f = open(filename, 'w')
  f.write('Minimize\n') 
  f.write('\tvalue: ')
  
  # Objective function
  try:
    weight = [0]*num_resources
    for i in range(1, num_resources):
      weight[i] = weight[i-1]*reservation_size + 1
    out = ""
    for R in resources:
      for r in reservation:
	if r.type == R.type:
	  out = out + str(weight[int(R.id)]) + " " + r.key + "_" + R.key + " + "
    f.write(out)
    f.seek(-3, 2) # remove last " + "
    f.write('\n')
  except Exception, e:
    print "Exception in LP generation (objective function): %s" % e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    raise

  f.write("Subject To\n")
  
  # Linear constrains
  try:
    # Unicity constrains
    for r in reservation:
      f.write("\tunicity" + r.key + ": ")
      for R in resources:
	if r.type == R.type:
	  f.write(r.key + "_" + R.key + " + ")
      f.seek(-3, 2)
      f.write (" = 1\n")
  except Exception, e:
    print "Exception in LP generation (unicity contranints): %s" % e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    raise
  
  try:
    # Capacity constrains 
    for R in resources:
      for a in R.attributes:
	out = ""
	for r in reservation:
	  if r.type == R.type:
	    if a in r.attributes:
	      out = out + str(r.attributes[a]) + " " + r.key + "_" + R.key + " + "
	if out != "":
	  out = "\t" + a + "_" + R.key + ": " + out
	  f.write(out)
	  f.seek(-3, 2)
	  f.write(" <= " + str(R.attributes[a]) + "\n")
  except Exception, e:
    print "Exception in LP generation (capacity constrains): %s" % e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    raise
      
  try:
    # " - Compound Resources"
    links = set() # the ids of compound resources (link between two resources)
    attr_bounds = "" # stores all the bounds for compound attributes (Bounds are added to the LP at the end)

    for ca in compound_attributes:
      #"Generating compound capacity constraints:"
      for j in range(num_resources):
	R = resources[j]
	for jp in range(j+1, num_resources):
	    Rp = resources[jp]
	    addends = "" # stores ADDENDS in each constraint
	    for i in range(reservation_size):
	      r = reservation[i]
	      acc = 0
	      accp = 0
	      out = ""
	      outp = ""
	      for ip in range(i+1, reservation_size):
		rp = reservation[ip]
		if compound_reservation[i][ip] != None and compound_reservation[i][ip][ca] != None:
		  if rp.type == Rp.type:
		    acc = acc + int(compound_reservation[i][ip][ca]["Value"])
		    out = out + str(compound_reservation[i][ip][ca]["Value"]) + " " + rp.key + "_" + Rp.key + " + "
		  if rp.type == R.type:
		    accp = accp + int(compound_reservation[i][ip][ca]["Value"])
		    outp = outp + str(compound_reservation[i][ip][ca]["Value"]) + " " + rp.key + "_" + R.key + " + "
	      if  acc > 0:
		if r.type == R.type:
		  f.write("\t"+ ca + R.key + Rp.key + r.key + R.key +": "+ `acc` + " " + r.key + "_" + R.key + " + " + out)
		  f.seek(-3, 2)
		  f.write(" - " + ca + "_" + R.key + Rp.key + r.key + R.key + " <= " + `acc` + "\n") 
		  addends = addends + ca + "_" + R.key + Rp.key + r.key + R.key + " + "
		  attr_bounds = attr_bounds + "\t0 <= " + ca + "_" + R.key + Rp.key + r.key + R.key + " <= " + `acc` + "\n"
	      if accp > 0:
		if r.type == Rp.type:
		  f.write("\t"+ ca + R.key + Rp.key + r.key + Rp.key +": " + `accp` + " " + r.key + "_" + Rp.key + " + " + outp)
		  f.seek(-3, 2)
		  f.write(" - " + ca + "_" + R.key + Rp.key + r.key + Rp.key + " <= " + `accp` + "\n") 
		  addends = addends + ca + "_" + R.key + Rp.key + r.key + Rp.key + " + "
		  attr_bounds = attr_bounds + "\t0 <= " + ca + "_" + R.key + Rp.key + r.key + Rp.key + " <= " + `accp` + "\n"
	    if len(addends) > 0:
	      print "::::>", str(compound_resources)
	      f.write("\t" + compound_resources[j][jp].key + "_" + ca + ": " + addends)
	      f.seek(-3, 2)
	      f.write(" - " + str(compound_resources[j][jp].key) + "_" + ca + " = 0\n")
	      links = links | {compound_resources[j][jp].key} 
	      
      if links: # Adding compound resources constrains # TODO Needs to be check, currently these constrains are not passed
	for c in constraints:
	  out = ""
	  written = False
	  for a in c.addends:
	    if a in links:
	      written = True
	      out = out + `a` + " + "
	  if written:
	    out = out[:-3] # remove last " + "
	    out = "\t" + c.key + "_" + c.attribute + ": " + out + " " + c.operation + " " + `c.threshold` + "\n";
	  f.write(out)

  except Exception, e:
    print "Exception in constraint physical links %s" % e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    raise
  
  try:
  # - Generating distance constrains:"
    for da in distance_attributes:
      for i in range(reservation_size):
	r = reservation[i]
	for j in range(num_resources):
	  R = resources[j]
	  if r.type == R.type:
	    ND = [ ]
	    for jp in range(num_resources):
	      if j != jp:
		Rp = resources[jp]
		for ip in range(i+1, reservation_size):
		  rp = reservation[ip]	  
		  if rp.type == Rp.type and distances[i][ip] != None and distances[i][ip][da] != None:
		    if (j < jp and float(compound_resources[j][jp].attributes[da]) > float(distances[i][ip][da])) or (jp < j and float(compound_resources[jp][j].attributes[da]) > float(distances[i][ip][da])):
		      ND.append(rp.key + "_" + Rp.key)
	    if len(ND) > 0:
	      f.write("\tdistance" + r.key + "_" + R.key + ": " + str(len(ND)) + " " + r.key + "_" + R.key + " + ")
	      for x in ND:
		f.write(str(x) + " + ")
	      f.seek(-3, 2) # remove last " + "
	      f.write(" <= "+str(len(ND)) +"\n")
  except Exception as e:
    print "Exception in distance constraints: %s" % e
    print "compound resources = " + str(compound_resources)
    print "distances = " + str(distances)
    
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    raise


  
  try:
    # Generate bounds for compound attributes
    out = ""
    for ca in compound_attributes:	    
     for j in range(num_resources):
	for jp in range(j+1, num_resources):
	  out = out + "\t0 <= " + compound_resources[j][jp].key + "_" + ca + " <= " + `compound_resources[j][jp].attributes[ca]` + "\n"
    out = out + attr_bounds
    if out != "":
      f.write("Bounds\n"+out);
    
  except Exception, e:
    print "Exception in bounds: %s" % e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    raise
  
  f.write("Binary\n\t")
  for r in reservation:
    for R in resources:
      if r.type == R.type:
	f.write(r.key+"_"+R.key+" ")
  f.seek(-1, 2) # remove last space " "
  f.write("\nEnd\n")
  f.close();


def generate_reservations(solution, resources, reservation, resources_table, compound_resources_table):
  result = [None]*len(reservation)
  
  try:
    # Generate reservations of single resources
    for s in solution:
      if s[0] == 'r' and solution[s] > 0 :
	keys = s.split('_')
	R = resources[resources_table[keys[1]]]
	result[int(keys[0][1:])] = {"manager": R.irm, "res_id": R.key, "alloc_req": reservation[int(keys[0][1:])]}

    # Remove None elements in reservation array  
    result = [x for x in result if x != None]
    
    # Generate reservations of compound resources
    for s in solution:
      if s[0] == 'l' and solution[s] > 0 :
	keys = s.split('_')
	R = compound_resources_table[keys[0]]
	result.append({"manager": R.irm, "res_id": R.key, "alloc_req": {'Type': 'Network Link', 'Attributes': {keys[1]: solution[s]}}})
	
  except Exception, e:
    print "Exception in generate_reservations: %s" % e
    print str(resources)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    raise
  return result
 
def encode_resource_names(resources):
   _resources = copy.deepcopy(resources)
   _encdict = { }
   for m in _resources:
      res = _resources[m]
      for r in res:
         key = r.replace("-", "")
         if (key != r):
            if m not in _encdict:
                _encdict[m] = {}
            _encdict[m][key] = r
            res[key] = res[r]
            del res[r]
   return _resources, _encdict
   
def decode_resource_names(result, enc_dict):  
  
   for r in result:
      if r['manager'] in enc_dict:
         if r['res_id'] in enc_dict[r['manager']]:
             r['res_id'] = enc_dict[r['manager']][r['res_id']]
                
@staticmethod
def schedule(managers, resources,  alloc_req, constrains, res_constrains):
   try:  
   
      group_counter = 1000

      # managers: list of managers (not used)
      #print "managers: " + `managers`
      # resources: list of resources of each Manager
      #print "resources: " + `resources`
      # res_constrains: constrains relating several resources
      # alloc_req: an allocation request
      #print "alloc_req: " + `alloc_req`
      # constrains: distance constrains
      #print "constrains: " + `constrains`
      
      reservation = alloc_req 
      
      resources,enc_dict = encode_resource_names(resources)
      
	
      # Translate resources to generate the optimization problem
      resources_aux = [ ]
      resources_table = { } # used to find the internal id of a resource (integer) using the id given by the IRM
      idx = 0
      for irm in resources:
	for R in resources[irm]:
	  if not "Source" in resources[irm][R]["Attributes"]: # The resource is not a compound resource
	    newR = Resource(idx)
	    resources_table[R] = idx
	    newR.irm = irm
	    newR.key = R
	    newR.type = resources[irm][R]["Type"]
	    newR.attributes = { }
	    for a in resources[irm][R]["Attributes"]:
	      newR.attributes[a] = resources[irm][R]["Attributes"][a]
	    resources_aux.append(newR)
	    idx = idx + 1
      
      # Translate compound resources to generate the optimization problem   
      # This implementation assumes only 1 type of compound resources, i.e. Network Links
      compound_resources = [[None]*len(resources_aux) for _ in range(len(resources_aux))]
      compound_resources_table = { }
      for irm in resources:
	for R in resources[irm]:
	  if "Source" in resources[irm][R]["Attributes"]: # The resource is a compound resource
	    
	    source = resources_table[resources[irm][R]["Attributes"]["Source"]] 
	    target = resources_table[resources[irm][R]["Attributes"]["Target"]] 
	    if target < source:
	      aux = source
	      source = target
	      target = aux
	    compound_resources[source][target] = Resource(idx)
	    compound_resources[source][target].key = R
	    compound_resources[source][target].irm = irm
	    compound_resources_table[R] = compound_resources[source][target] # save resource in table to get fast access by key
	    idx = idx + 1
	    for a in resources[irm][R]["Attributes"]:
	      compound_resources[source][target].attributes[a] = resources[irm][R]["Attributes"][a]
      
      # Translate resource constrains to generate the optimization problem
      res_constrains_aux = { }
      idx = 0
      for irm in res_constrains:
	for c in res_constrains[irm]:
	  constraint = res_constrains[irm][c]["Constraint"]
	  attribute = res_constrains[irm][c]["Attribute"]
	  #operation = res_constrains[irm][c]["Operation"]
	  #threshold = res_constrains[irm][c]["Threshold"]
	  if attribute not in res_constrains_aux:
	    res_constrains_aux[attribute] = [ ]
	  newC = Constraint(idx)
	  newC.operation = " <= "
	  split_cons = constraint.split("<=")
	  newC.threshold = split_cons[1]
	  newC.addends = map(lambda x: x.strip(), split_cons[0].split("+"))
	  
	  # Gabriel (4/08/2015): Please check if this is correct:      
	  res_constrains_aux[attribute].append(newC)
	  idx = idx + 1

      # Translate allocation request to generate the optimization problem
      reservation_aux = [ ]
      inverse_resources = { } # used to find the internal id of a resource (integer) using the id given by the IRM
      groups = { }
      idx = 0
      for r in alloc_req:
	if "Source" not in r["Attributes"]: 
	  newr = Resource(idx)
	  newr.id = idx
	  newr.key = "r" + `idx`
	  if "Group" not in r:
	     r["Group"] = "GRP" + str(group_counter)
	     group_counter = group_counter + 1
	      
	  newr.group = r["Group"]
	  if newr.group not in groups:
	    groups[newr.group] =  [ ]
	  groups[newr.group].append(idx)
	  inverse_resources[newr.key] = idx
	  newr.type = r["Type"]
	  newr.attributes = { }
	  for a in r["Attributes"]:
	    newr.attributes[a] = r["Attributes"][a]
	  reservation_aux.append(newr)
	  idx = idx + 1 
      
      # Translate compound allocation request to generate the optimization problem
      compound_reservation = [[None]*len(reservation_aux) for _ in range(len(reservation_aux))]
      compound_attributes = set()
      for r in alloc_req:
	if "Source" in r["Attributes"]: # The resource is a compound resource
	  source = r["Attributes"]["Source"]
	  target = r["Attributes"]["Target"]
	  #operation = d["ConstraintType"]
	  for i in groups[source]:
	    for ip in groups[target]:
		if i < ip:
		  compound_reservation[i][ip] = {}  
		if ip < i:
		  compound_reservation[ip][i] = {}  
		for a in r["Attributes"]:
		  if a != "Source" and a != "Target":
		    if a not in compound_attributes:
		      compound_attributes = compound_attributes | {a}
		    if i < ip:
		      compound_reservation[i][ip][a] = { }
		      compound_reservation[i][ip][a]["Key"] = "r"+str(idx) 
		      compound_reservation[i][ip][a]["Value"] = r["Attributes"][a]  
		    if ip < i:
		      compound_reservation[ip][i][a] = { }
		      compound_reservation[ip][i][a]["Key"] = "r"+str(idx) 
		      compound_reservation[ip][i][a]["Value"] = r["Attributes"][a]
		    idx = idx + 1 

      # Translate distance constrains request to generate the optimization problem
      distances_aux = [[None]*len(reservation_aux) for _ in range(len(reservation_aux))]
      distance_attributes = set()
      for d in constrains:
	source = d["Source"]
	target = d["Target"]
	#operation = d["ConstraintType"]
	for i in groups[source]:
	  for ip in groups[target]:
	      if i < ip:
		distances_aux[i][ip] = {}  
	      if ip < i:
		distances_aux[ip][i] = {}  
	      for a in d:
		if a != "Source" and a != "Target" and a != "ConstraintType":
		  if a not in distance_attributes:
		    distance_attributes = distance_attributes | {a}
		  if i < ip:
		    distances_aux[i][ip][a] = d[a]  
		  if ip < i:
		    distances_aux[ip][i][a] = d[a]  
    
      result = []
      
      # Generates linear optimization problem
      generate_lp("crs.lp", resources_aux, compound_resources, res_constrains_aux, reservation_aux, compound_reservation, distances_aux, compound_attributes, distance_attributes) 
      
      # Creates GLPK object, solves the problem and gets the solution
      lp = glpk("crs.lp")
      value = lp.solve()
      solution = lp.solution()

      # Checks if GLPK found a solution
      if glp_get_status(lp._lp) != 5:
	print "Solution not found" # (or whatever else to indicate it)
      else:
	# Generates result
	result = generate_reservations(solution, resources_aux, reservation, resources_table, compound_resources_table)
	decode_resource_names(result, enc_dict)
	print "result = " + str(result)
      return result
   except Exception, e:
    print "Exception in schedule: %s" % e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    raise

               
         
         
               
      
      

   
