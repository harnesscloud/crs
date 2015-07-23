#!/usr/bin/env python

import sys
import os

LOC=os.path.dirname(os.path.realpath(__file__))

locations=[LOC+'/../../harness-resource-manager', LOC + '/harness-resource-manager']

for loc in locations:
   sys.path.append(loc)
   

