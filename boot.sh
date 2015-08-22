#!/bin/bash
sudo supervisorctl restart crs
sudo  supervisorctl restart irm-net
sudo  supervisorctl restart irm-nova irm-neutron



