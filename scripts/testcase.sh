#!/bin/bash

SCRIPTDIR=$PWD

####### Service Test ############
# Give a simple test, insert 100 messages, 10 message at the same time, cycle 10 times
cd $SCRIPTDIR
python3 service_test.py

# Pressure Test
#ab -n 10000 -c 100 http://localhost/index.php

####### Security Test ############
# Check Serurity Prolicy active or not 
cd $SCRIPTDIR
python3 security_test.py