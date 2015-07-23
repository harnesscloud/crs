import pytest
import subprocess
import os
import requests
import time
import json

LOC=os.path.dirname(os.path.realpath(__file__))

CRS="http://localhost:56770/v3"

def post(method, data={}):
   return requests.post(CRS + method, data=json.dumps(data) )
   
def get(method):
   return requests.get(CRS + method)   

def delete(method, data={}):
   return requests.delete(CRS + method, data=json.dumps(data) )
 

def load_services():
   global crs, irm_nova
   
   # just in case...
   os.system("pkill -f app.py")
   os.system("pkill -f irm-nova.py")

   print "loading services..." 
   crs = subprocess.Popen([LOC +"/../../crs/app.py", "-p", "56770"], cwd=LOC +"/../../crs")
   irm_nova = subprocess.Popen([LOC +"/../../../irm-nova/irm-nova.py", "-m", "-c", LOC+"/irm-vagrant-test.cfg"], cwd=LOC +"/../../../irm-nova")   
   time.sleep(1)
 
def unload_services():
   global crs, irm_nova
   print "unloading services..."
   crs.terminate()
   irm_nova.terminate()
   
   
@pytest.fixture(autouse=True, scope="module")
def init(request):
   load_services()
   def end():
      unload_services()
            
   request.addfinalizer(end)
   

def test1():
   r = requests.get(CRS + "/managers")
   assert r.status_code == 200
   assert r.json()["result"][0]["Name"] == "IRM-NOVA" 
   r = delete("/reservations/all") 
   assert r.status_code == 200
   assert "error" not in r.json()
   
   r = requests.get(CRS + "/resources/alloc-spec")
   assert r.status_code == 200
   ss = r.json()
   assert "result" in ss
   assert "Machine" in ss["result"]["Types"]
  
def test2():

   # create reservation
   r = post("/reservations", { "Allocation": [ { "Type": "Machine", \
                               "Attributes": {"Cores": 1, "Memory": 2000  } } ] })
   assert r.status_code == 200
   rs = r.json()   
   assert "result" in rs
   assert len(rs["result"]["ReservationID"]) == 1
   resID = rs["result"]["ReservationID"][0]

   # check reservation
   r = post("/reservations/check", { "ReservationID": [resID] })
   assert r.status_code == 200
   rs = r.json()
   assert "result" in rs and rs["result"]["Instances"][resID]["Ready"] == "True"
   
   time.sleep(1)
   # release reservation
   r = delete("/reservations", { "ReservationID": [resID] })   
   assert r.status_code == 200
   rs = r.json()
   assert "result" in rs

# two requests   
def test3():
   # create reservation
   r = post("/reservations", { "Allocation": [ { "Type": "Machine", \
                               "Attributes": {"Cores": 1, "Memory": 2000  } },\
                                               { "Type": "Machine", \
                               "Attributes": {"Cores": 3, "Memory": 3000  } }] })
   assert r.status_code == 200
   rs = r.json()   
   assert "result" in rs
   assert len(rs["result"]["ReservationID"]) == 1
   resID = rs["result"]["ReservationID"][0]

   # check reservation
   r = post("/reservations/check", { "ReservationID": [resID] })
   assert r.status_code == 200
   rs = r.json()
   assert "result" in rs and rs["result"]["Instances"][resID]["Ready"] == "True"
   time.sleep(1) 
   # release reservation
   r = delete("/reservations", { "ReservationID": [resID] })   
   assert r.status_code == 200
   rs = r.json()
   assert "result" in rs     

# requests with metrics   
def test4(): 
   # create reservation
   r = post("/reservations", { "Allocation": [ { "Type": "Machine", \
                               "Attributes": {"Cores": 1, "Memory": 2000  } } ], \
                               "Monitor": { \
                                   "Machine": { \
                                       "CPU_U_S_TIME": { "PollTimeMultiplier": 1 }, \
                                       "MEM_U_S_BYTE": { "PollTimeMultiplier": 1 }, \
                                       "MEM_TOT_BYTE": { "PollTimeMultiplier": 1 }, \
                                       "CPU_TOT_TIME": { "PollTimeMultiplier": 1 } \
                                   },"PollTime": 1}}) 
   assert r.status_code == 200
   rs = r.json()  
   assert "result" in rs
   assert len(rs["result"]["ReservationID"]) == 1
   resID = rs["result"]["ReservationID"][0]                              
   
   time.sleep(2)
   r = get("/metrics?id="+resID+"&entry=1")
   assert r.status_code == 200
   rs = r.json()
   assert "result" in rs
   assert "Metrics" in rs["result"]
   assert "CPU_U_S_TIME" in rs["result"]["Metrics"]
   
   # release reservation
   r = delete("/reservations", { "ReservationID": [resID] })   
   assert r.status_code == 200
   rs = r.json()
   assert "result" in rs      
   
