import yaml
from inspect import modulesbyfile
from tokenize import Name
from unicodedata import name
import click
import yaml


values = """
name: {shit}
#fullname:
replicaCount: {replicacount}

images:
  PullSecrets: {pullsecret}
  repository: {repo}
  tag: {tag}

config:
  configmaps: {configmap}
  env:
  - name: MESSAGE
    value: 'did work'

service:
  type: ClusterIP

ingress:
  enabled: {ingress}
  hosts:
  - host: {host}
    paths:
      - path: {path}
        service: {serviceIngress}
        port: {port}
    """
# helmfile = """
# environments:
#   dev:
#   prod:

# repositories:
# - name: yesodot
#   url: https://harborreg-2.northeurope.cloudapp.azure.com/chartrepo/library
#   username: {{ requiredEnv "HARBOR_USER" }}
#   password: {{ requiredEnv "HARBOR_PASSWORD" }}
  
# releases:
# - name: {serviceName}
#   namespace: {namespace}
#   chart: yesodot/common
#   version: {{ requiredEnv "COMMON_VERSION" | default "0.5.2" }}
#   values:
#     - ./values.yaml

# helmDefaults:
#   recreatePods: true
#   createNamespace: true
#     """

service = """
service:
  type: ClusterIP
  ports:
  - name: {}
    port: {}
    """


shit = input('enter name ')
namespace = input('enter name space ')
replicacount = int (1)
replicacount = int (input('enter replica count  '))
pullsecret = input('enter pullsecret name  ')
repo = input('enter your repo  ')
tag = 'latest' 
tag = input('enter tag  ')
configmap =[]
configmap = input('enter configmap name  ')
###ingress###
ingress = False
ingress = bool (input('enter true or false to ingress  '))
path = '/'
path = input('enter path to ingress ')
port = int (3000) 
port = int (input('enter port to ingress service '))
host = 'example'
host = input('enter host to ingress  ')
serviceIngress = input ('enter service name to ingress')
def wri(shit, replicacount, pullsecret, repo, tag ,configmap, ingress, host, path, serviceIngress,port):
    with open('values.yaml', 'w') as yfile:
        docs = yaml.load(values.format(shit, replicacount, pullsecret, repo, tag ,configmap, ingress, host, path, serviceIngress,port))
        yaml.dump (docs ,yfile)
        # with open('helmfile.yaml', 'w') as yfile:
        #     yfile.write(helmfile.format(shit, namespace, replicacount, pullsecret, repo, tag ,configmap, ingress, path, port, host))



###sservice###
serviceCount = 1
serviceCount = int (input('enter count to services '))
count =0
wri(shit, replicacount, pullsecret, repo, tag ,configmap, ingress, host, path, serviceIngress,port )
while count < serviceCount:
    # for i in serviceCount:
    serviceName = input('enter name to service ')
    servicePort = int  (input('enter port to service  '))
    count = count + 1
    with open(shit+'-values.yaml', 'a') as yfile:
        docs = yaml.load(service.format(serviceName, servicePort,Loader=yaml.FullLoader))
        yaml.dump(docs,yfile )





