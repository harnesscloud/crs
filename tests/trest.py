#!/usr/bin/env python

import json, requests, sys

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

def expect(name, lfn, API, fn, data={}):
   try:
      test = TRapi(API)
      print "TEST [" + name + "]: ",
      sys.stdout.flush()
      ret = test.connect(fn, data)
      if not lfn(ret):
         print "FAILED!"
         print "Received [" + str(ret) + "]"
         exit(-1)
      else:
         print "SUCCESS!"
         return ret
	
   except Exception, msg:
      print "ERROR!: " + str(msg)
      exit(-1)



