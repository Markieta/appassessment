#!/bin/bash
# login to the oc cli using the pod's serviceaccount token
oc login --token=`cat /var/run/secrets/kubernetes.io/serviceaccount/token` --server=https://kubernetes.default.svc
# set the now variable to the current date
now=$(date +"%m_%d_%Y")
# run the python script with the TARGET_NAMESPACE variable and output to the expected PVC
python ./report.py -n ${TARGET_NAMESPACE} -o /output/report-${now}.html