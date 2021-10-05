import json
from os import write
import sys
import logging
from datetime import datetime
from jsonpath_ng import jsonpath, parse
from plumbum import local
import argparse
import yaml


def getObjects(type, namespace='default'):
  try: 
    oc = local["oc"]
    data = json.loads(oc('get', type, '-n', namespace, '-o', 'json'))
    logging.info("read objects data of type " + type)
  except:
    logging.error("unable to read object data of type " + type)
    return []

  if "items" in data.keys():
    return data["items"]

  return []
#end

def declarativeComponentCheck(workloadData):
  retval = {'color': 'red', 'text': workloadData['kind']}
  if workloadData['kind'] in ['CronJob', 'DaemonSet', 'Deployment', 'StatefulSet', 'DeploymentConfig']:
    retval['color'] = 'green'

  return retval
#end

def rollingUpdateCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  first = parse('spec.strategy.type').find(workloadData)
  second = parse('spec.updateStrategy.type').find(workloadData)
  if ((len(first) == 1) and (first[0].value == "RollingUpdate")) or ((len(second) == 1) and (second[0].value == "RollingUpdate")):
    retval['color'] = 'green'
    retval['text'] = 'RollingUpdate'
  else:
    retval['color'] ='red'

  return retval
#end

def cpuRequestCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].resources.requests.cpu').find(workloadData)
  if (len(matches) > 0) and (len(matches) == len(workloadData['spec']['template']['spec']['containers'])):
    retval['color'] = 'green'
    container_cpu_requests = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_cpu_requests = container_cpu_requests + [{'container_name': container['name'], 'cpu_request': container['resources']['requests']['cpu']}]
    retval['text'] = yaml.dump(container_cpu_requests)
  else:
    retval['color'] = 'red'

  return retval
#end

def memoryRequestCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].resources.requests.memory').find(workloadData)
  if (len(matches) > 0) and (len(matches) == len(workloadData['spec']['template']['spec']['containers'])):
    retval['color'] = 'green'
    container_memory_requests = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_memory_requests = container_memory_requests + [{'container_name': container['name'], 'memory_request': container['resources']['requests']['memory']}]
    retval['text'] = yaml.dump(container_memory_requests)
  else:
    retval['color'] = 'red'

  return retval
#end

def cpuLimitCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].resources.limits.cpu').find(workloadData)
  if (len(matches) > 0) and (len(matches) == len(workloadData['spec']['template']['spec']['containers'])):
    retval['color'] = 'green'
    container_cpu_limits = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_cpu_limits = container_cpu_limits + [{'container_name': container['name'], 'cpu_limit': container['resources']['limits']['cpu']}]
    retval['text'] = yaml.dump(container_cpu_limits)
  else:
    retval['color'] = 'red'

  return retval
#end

def memoryLimitCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].resources.limits.memory').find(workloadData)
  if (len(matches) > 0) and (len(matches) == len(workloadData['spec']['template']['spec']['containers'])):
    retval['color'] = 'green'
    container_memory_limits = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_memory_limits = container_memory_limits + [{'container_name': container['name'], 'memory_limit': container['resources']['limits']['memory']}]
    retval['text'] = yaml.dump(container_memory_limits)
  else:
    retval['color'] = 'red'

  return retval
#end

def livenessProbeCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].livenessProbe').find(workloadData)
  noEmptyProbes = True
  for match in matches:
    if len(match.value.keys()) == 0:
      noEmptyProbes = False

  if (len(matches) > 0) and noEmptyProbes and (len(matches) == len(workloadData['spec']['template']['spec']['containers'])):
    retval['color'] = 'green' 
    container_liveness_probes = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_liveness_probes = container_liveness_probes + [{'container_name': container['name'], 'livenessProbe': container['livenessProbe']}]
    retval['text'] = yaml.dump(container_liveness_probes)
  else: 
    retval['color'] = 'red'
  
  return retval
#end

def readinessProbeCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].readinessProbe').find(workloadData)
  noEmptyProbes = True
  for match in matches:
    if len(match.value.keys()) == 0:
      noEmptyProbes = False

  if (len(matches) > 0) and noEmptyProbes and (len(matches) == len(workloadData['spec']['template']['spec']['containers'])):
    retval['color'] = 'green'
    container_readiness_probes = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_readiness_probes = container_readiness_probes + [{'container_name': container['name'], 'readinessProbe': container['readinessProbe']}]
    retval['text'] = yaml.dump(container_readiness_probes)
  else:
    retval['color'] = 'red'

  return retval
#end

def statelessCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.volumes[*].persistentVolumeClaim').find(workloadData)
  if (len(matches) > 0):
    retval['color'] = 'yellow'
    pvcList = []
    for match in matches:
      pvcList = pvcList + [match.value]

    retval['text'] = yaml.dump(pvcList)
  else:
    retval['color'] = 'green'
  
  return retval
#end

def hpaCheck(workloadData):
  retval = {'color': 'red', 'text': ''}
  jsonpath_expr = parse('spec.scaleTargetRef')
  for hpa in hpaObjects:
    if retval['color'] == 'green':
      break
    #end

    matches = jsonpath_expr.find(hpa)
    for match in matches:
      try: 
        if (match.value['kind'] == workloadData['kind']) and (match.value['name'] == workloadData['metadata']['name']):
          retval['color'] = 'green'
          retval['text'] = yaml.dump(match.value)
          break
        #end
      except:
        pass
      #end
    #end
  #end

  return retval
#end

def pdbCheck(workloadData):
  retval = {'color': 'red', 'text': ''}
  jsonpath_expr = parse('spec.selector.matchLabels')
  for pdb in pdbObjects:
    if retval['color'] == 'green':
      break
    #end

    matches = jsonpath_expr.find(pdb)
    for match in matches:
      try: 
        if (match.value == workloadData['spec']['selector']['matchLabels']):
          retval['color'] = 'green'
          retval['text'] = yaml.dump(match.value)
          break
        #end
      except:
        pass
      #end
    #end
  #end

  return retval
#end

def writeReport(filename, results):
  file = open(filename, 'w')
  file.write("<html>\n")
  file.write("<head>\n")
  file.write("<style>\ntable, th, td {\n  border: 1px solid black;\n}\n</style>\n")
  file.write("<title>report generated on " + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "</title>\n")
  file.write("</head>\n")
  file.write("<body>\n")

  file.write("<hr>\n")
  file.write("<table>\n")

  workloadNames = results[next(iter(results))].keys()
  file.write("<tr>\n")
  file.write("<td>Target</td>")
  for workloadName in workloadNames:
    file.write("<td>" + workloadName + "</td>")
  file.write("\n</tr>\n")

  for checkName in results.keys():
    file.write("<tr>\n<td>"+checkName+"</td>")
    for workloadName in results[checkName].keys():
      file.write("<td style=\"background-color: " + results[checkName][workloadName]['color'] + "\"></td>")

    file.write("\n</tr>\n")
  #end

  file.write("</table>\n")
  file.write("<hr>\n")

  for workloadName in workloadNames:
    file.write("<table>\n")
    file.write("<tr><td>Target</td><td>" + workloadName + "</td></tr>\n")

    for checkName in results.keys():
      file.write("<tr><td>"+checkName+"</td><td style=\"background-color: " + results[checkName][workloadName]['color'] + "\"><pre>" + results[checkName][workloadName]['text'] + "</pre></td></tr>\n")

    file.write("</table>\n")
    file.write("<hr>\n")

  file.write("</body>\n")
  file.write("</html>\n")
  file.close()
#end


parser = argparse.ArgumentParser()
parser.add_argument("-l", help="log file name", type=str, default="report.log")
parser.add_argument("-o", help="output file name", type=str, default="report.html")
parser.add_argument('-n', help="namespace", type=str, default="default")
args = parser.parse_args()

logging.basicConfig(filename=args.l, level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d-%H:%M:%S')
logging.info("generating report")

namespace = args.n
if namespace == "default":
  validNS = True
else:
  validNS = False
  namespaceList = getObjects('namespace', 'default')
  for nsObj in namespaceList:
    if nsObj['metadata']['name'] == namespace:
      validNS = True
      break
    #end
  #end
#end


if not validNS:
  logging.error(namespace + " is not a valid namespace")
  sys.exit("error: " + namespace + " is not a valid namespace")
#end

workloadObjects = getObjects('cronjobs', namespace) + getObjects('daemonset', namespace) + getObjects('deployment', namespace) + getObjects('statefulset', namespace) + getObjects('deploymentconfig', namespace)
if len(workloadObjects) == 0:
  message = "unable to find any cronjobs, daemonsets, deployments, statefulsets or deploymentconfigs in namespace " + namespace + ".  Report not generated"
  logging.info(message)
  print(message)
  sys.exit()
#end

hpaObjects = getObjects('hpa', namespace)
pdbObjects = getObjects('poddisruptionbudgets', namespace)

checks = {}
checks["declarativeComponentCheck"] = declarativeComponentCheck
checks["RollingUpdateCheck"] = rollingUpdateCheck
checks["CPURequestCheck"] = cpuRequestCheck
checks["MemoryRequestCheck"] = memoryRequestCheck
checks["CPULimitCheck"] = cpuLimitCheck
checks["MemoryLimitCheck"] = memoryLimitCheck
checks["LivenessProbeCheck"] = livenessProbeCheck
checks["ReadinessProbeCheck"] = readinessProbeCheck
checks["StatelessCheck"] = statelessCheck
checks["HPACheck"] = hpaCheck
checks["PDBCheck"] = pdbCheck

results = {}
for checkName in checks.keys():
  results[checkName] = {}
  for workload in workloadObjects:
    workloadName = workload['metadata']['name']
    logging.info("running check " + checkName + " on workload " + workloadName)
    results[checkName][workloadName] = checks[checkName](workload)

writeReport(args.o, results)
