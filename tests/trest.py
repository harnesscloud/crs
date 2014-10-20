#!/usr/bin/env python

import json, requests

class TRapi:
   def __init__(self, api):
      self.api = api
      
   def connect(self, fn, data={}):
        
      headers = {'content-type': 'application/json'}
      ret = json.dumps(data)
 	
      r = requests.post(self.api+'/method/'+fn, ret, headers=headers)
  
      if (r.status_code != 200):
         raise Exception("error found: " + str(r.status_code) + ":" + str(r.json()))
      return r.json()

def p(fn, API, data={}):
   try:
      test = TRapi(API)
      ret = test.connect(fn, data)
      print "SUCCESS: ", ret
   except Exception, msg:
      print "ERROR!: " + str(msg)

def expect(name, lfn, API, fn, data={}):
   try:
      test = TRapi(API)
      ret = test.connect(fn, data)
      if not lfn(ret):
         print "TEST [" + name + "]: FAILED!"
         print "Received [" + str(ret) + "]"
         exit(-1)
      else:
         print "TEST [" + name + "]: SUCCESS!"
         return ret
	
   except Exception, msg:
      print "TEST [" + name + "]: ERROR!: " + str(msg)
      exit(-1)



