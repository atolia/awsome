#!/usr/bin/env python

import yaml, json, boto3, sys, urllib3
from kubernetes import client, config
from pprint import pprint as pp
from datetime import datetime as dt
from util import eprint
from util import age

def image_name(c):
  return '/'.join( c.split('/')[1:] or [c] ).split(':')[0] 

def image_tag(c):
  return (c.split(':')[1:] or [''])[0]

def additional_tags( repo, hashsum):
  if repo in repos:
    for i in repos[repo]:
      if i['imageDigest'] == 'sha256:' + hashsum:
        return [ j for j in i['imageTags'] if (not 'PRE-' in j and not 'PROD-' in j and not 'temp_' in j ) ] 
        # return i['imageTags']
    return []
  else:
    return []

def containers(pod, now):
  ret=[]
  for j,c in zip(range(len(pod.status.container_statuses)), pod.status.container_statuses ):
    ret.append ( {
        'image': { 
            'name': image_name(pod.spec.containers[j].image ),
            'tag': image_tag(pod.spec.containers[j].image ),
            'other_tags': 
               additional_tags( image_name(pod.spec.containers[j].image), (c.image_id+'::').split(':')[2]  )
            , 'hash': (c.image_id+'::').split(':')[2]
            , 'hash_short': (c.image_id+'::').split(':')[2][0:9]
        },
        'started': age(c.state.running.started_at, now) if hasattr( c.state.running,'started_at') else None,
        'ready': c.ready,
        'restarts': c.restart_count,
        'last_state': {'reason': c.last_state.terminated.reason, 'exit_code': c.last_state.terminated.exit_code} if hasattr( c.last_state.terminated,'reason') else None
    }  )
  return ret

def main():
  if len(sys.argv) < 2 :
    print( f'Usage: {sys.argv[0]} out.json\n')
    exit(1);  
  with open("config.yml", 'r') as stream:
    try:
      cfg=yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      eprint(exc)

  kube={}
  for con in cfg['clusters']:
    try:
      v1 = client.CoreV1Api(api_client=config.new_client_from_config(context=con))
    except Exception as exc:
      eprint(f'Unable to read k8s config from ~/.kube {exc}')
      exit(1)
    # get all pods but filter out cronJobs
    eprint(f'Fetching pods from {con}...')
    
    try:
      kube[con] = v1.list_pod_for_all_namespaces(field_selector='status.phase!=Succeeded,status.phase!=Failed').items
    except Exception as exc:
      eprint(f'Unable to connect to {con}: {exc}')
      exit(1)

  ecr = boto3.client('ecr')
  ecr_images=[]
  stages=[j for k,v in cfg['clusters'].items() for j in v['namespaces'] ]
  for con in cfg['clusters']:
    for n in kube[con]:
      if n.metadata.namespace in stages:
        for img in n.spec.containers:
          if '.amazonaws.com' in img.image:
            ecr_images.append( image_name(img.image))


  # uniq array of repos
  for e in set(ecr_images):
    eprint(f'Fetching ecr repos from {e}...')
    try:  
      res = ecr.describe_images(repositoryName=e, maxResults=1000, filter={ 'tagStatus': 'TAGGED'} )['imageDetails']
      # eprint(res)
    except Exception as exc:
      eprint(f'Unable to connect to AWS ECR: {exc}')
      eprint('Skipping additional tags check')
      break
    repos[e] = [ item for item in res if 'imageTags' in item ]

  now=dt.utcnow()
  for name, con in kube.items():
    for ns in cfg['clusters'][name]['namespaces']:
      pods=[item for item in con if item.metadata.namespace==ns]
      o =[ { 'id': i,
            'name': pod.metadata.name,
            'containers': containers(pod,now) 
          } for i,pod in zip(range(len(pods)),pods) ]
      cfg['clusters'][name]['namespaces'][ns]['pods']=o
  
      imgs={}
      for i, pod in zip( range(len(o)), o):
        for c in pod['containers']:
          if c['image']['name'] in imgs:
            imgs[c['image']['name']].append(i)
          else:
            imgs[c['image']['name']]=[i]    
      cfg['clusters'][name]['namespaces'][ns]['images']=imgs

  # print( json.dumps( { 'timestamp': now.strftime('%a %d %b %Y %H:%M UTC %Y'), 'clusters': cfg['clusters'] }, indent=2  ) )
  data = { 'timestamp': now.strftime('%a %d %b %Y %H:%M UTC %Y'), 'clusters': cfg['clusters'] }
  with open(sys.argv[1], 'w', encoding='utf-8') as outfile:
      json.dump(data, outfile, ensure_ascii=False, indent=2)


if __name__ == '__main__':
  urllib3.disable_warnings()
  repos={}
  main()

