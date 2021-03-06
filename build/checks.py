from jsonpath_ng import jsonpath, parse
import yaml

def notApplicableCheck(workloadData):
  return {'color': 'white', 'text': ''}
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
  if ((len(first) == 1) and ((first[0].value == "RollingUpdate") or (first[0].value == "Rolling"))):
    retval['color'] = 'green'
    retval['text'] = first[0].value
  elif ((len(second) == 1) and ((second[0].value == "RollingUpdate") or (second[0].value == "Rolling"))):
    retval['color'] = 'green'
    retval['text'] = second[0].value
  else:
    retval['color'] ='yellow'
    retval['text'] = 'In most cases the spec.strategy.type or spec.updateStrategy.type should be either "Rolling" or "RollingUpdate".  In stateful applications this not always possible.'

  return retval
#end

def cpuRequestCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].resources.requests.cpu').find(workloadData)
  numContainers = len(workloadData['spec']['template']['spec']['containers'])
  if (len(matches) > 0) and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_cpu_requests = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_cpu_requests = container_cpu_requests + [{'container_name': container['name'], 'cpu_request': container['resources']['requests']['cpu']}]
    retval['text'] = yaml.dump(container_cpu_requests)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have CPU requests specified.  All container specifications should include CPU requests"

  return retval
#end

def memoryRequestCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].resources.requests.memory').find(workloadData)
  numContainers = len(workloadData['spec']['template']['spec']['containers'])
  if (len(matches) > 0) and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_memory_requests = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_memory_requests = container_memory_requests + [{'container_name': container['name'], 'memory_request': container['resources']['requests']['memory']}]
    retval['text'] = yaml.dump(container_memory_requests)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have memory requests specified.  All container specifications should include memory requests"

  return retval
#end

def cpuLimitCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].resources.limits.cpu').find(workloadData)
  numContainers = len(workloadData['spec']['template']['spec']['containers'])
  if (len(matches) > 0) and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_cpu_limits = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_cpu_limits = container_cpu_limits + [{'container_name': container['name'], 'cpu_limit': container['resources']['limits']['cpu']}]
    retval['text'] = yaml.dump(container_cpu_limits)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have CPU limits specified.  All container specifications should include CPU limits"

  return retval
#end

def memoryLimitCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].resources.limits.memory').find(workloadData)
  numContainers = len(workloadData['spec']['template']['spec']['containers'])
  if (len(matches) > 0) and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_memory_limits = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_memory_limits = container_memory_limits + [{'container_name': container['name'], 'memory_limit': container['resources']['limits']['memory']}]
    retval['text'] = yaml.dump(container_memory_limits)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have memory limits specified.  All container specifications should include memory limits"

  return retval
#end

def cronjobCpuRequestCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.jobTemplate.spec.template.spec.containers[*].resources.requests.cpu').find(workloadData)
  numContainers = len(workloadData['spec']['jobTemplate']['spec']['template']['spec']['containers'])
  if (len(matches) > 0) and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_cpu_requests = []
    for container in workloadData['spec']['jobTemplate']['spec']['template']['spec']['containers']:
      container_cpu_requests = container_cpu_requests + [{'container_name': container['name'], 'cpu_request': container['resources']['requests']['cpu']}]
    retval['text'] = yaml.dump(container_cpu_requests)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have CPU requests specified.  All container specifications should include CPU requests"

  return retval
#end

def cronjobMemoryRequestCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.jobTemplate.spec.template.spec.containers[*].resources.requests.memory').find(workloadData)
  numContainers = len(workloadData['spec']['jobTemplate']['spec']['template']['spec']['containers'])
  if (len(matches) > 0) and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_memory_requests = []
    for container in workloadData['spec']['jobTemplate']['spec']['template']['spec']['containers']:
      container_memory_requests = container_memory_requests + [{'container_name': container['name'], 'memory_request': container['resources']['requests']['memory']}]
    retval['text'] = yaml.dump(container_memory_requests)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have memory requests specified.  All container specifications should include memory requests"

  return retval
#end

def cronjobCpuLimitCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.jobTemplate.spec.template.spec.containers[*].resources.limits.cpu').find(workloadData)
  numContainers = len(workloadData['spec']['jobTemplate']['spec']['template']['spec']['containers'])
  if (len(matches) > 0) and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_cpu_limits = []
    for container in workloadData['spec']['jobTemplate']['spec']['template']['spec']['containers']:
      container_cpu_limits = container_cpu_limits + [{'container_name': container['name'], 'cpu_limit': container['resources']['limits']['cpu']}]
    retval['text'] = yaml.dump(container_cpu_limits)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have CPU limits specified.  All container specifications should include CPU limits"

  return retval
#end

def cronjobMemoryLimitCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.jobTemplate.spec.template.spec.containers[*].resources.limits.memory').find(workloadData)
  numContainers = len(workloadData['spec']['jobTemplate']['spec']['template']['spec']['containers'])
  if (len(matches) > 0) and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_memory_limits = []
    for container in workloadData['spec']['jobTemplate']['spec']['template']['spec']['containers']:
      container_memory_limits = container_memory_limits + [{'container_name': container['name'], 'memory_limit': container['resources']['limits']['memory']}]
    retval['text'] = yaml.dump(container_memory_limits)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have memory limits specified.  All container specifications should include memory limits"

  return retval
#end


def livenessProbeCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].livenessProbe').find(workloadData)
  numContainers = len(workloadData['spec']['template']['spec']['containers'])
  noEmptyProbes = True
  for match in matches:
    if len(match.value.keys()) == 0:
      noEmptyProbes = False

  if (len(matches) > 0) and noEmptyProbes and (len(matches) == numContainers):
    retval['color'] = 'green' 
    container_liveness_probes = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_liveness_probes = container_liveness_probes + [{'container_name': container['name'], 'livenessProbe': container['livenessProbe']}]
    retval['text'] = yaml.dump(container_liveness_probes)
  else: 
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have a liveness probe defined.  All containers should have one."
  
  return retval
#end

def readinessProbeCheck(workloadData):
  retval = {'color': 'white', 'text': ''}
  matches = parse('spec.template.spec.containers[*].readinessProbe').find(workloadData)
  numContainers = len(workloadData['spec']['template']['spec']['containers'])
  noEmptyProbes = True
  for match in matches:
    if len(match.value.keys()) == 0:
      noEmptyProbes = False

  if (len(matches) > 0) and noEmptyProbes and (len(matches) == numContainers):
    retval['color'] = 'green'
    container_readiness_probes = []
    for container in workloadData['spec']['template']['spec']['containers']:
      container_readiness_probes = container_readiness_probes + [{'container_name': container['name'], 'readinessProbe': container['readinessProbe']}]
    retval['text'] = yaml.dump(container_readiness_probes)
  else:
    retval['color'] = 'red'
    retval['text'] = str(len(matches)) + " of " + str(numContainers) + " containers have a readiness probe defines.  All containers should have one."

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

    retval['text'] = "stateless application should not need a persistent volume.  The following persistent volume claims were found: \n" + yaml.dump(pvcList)
  else:
    retval['color'] = 'green'
  
  return retval
#end
