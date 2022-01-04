import click
import yaml




helmfile = """
environments:
  dev:
  prod:

repositories:
- name: yesodot
  url: https://harborreg-2.northeurope.cloudapp.azure.com/chartrepo/library
  username: {{ requiredEnv "HARBOR_USER" }}
  password: {{ requiredEnv "HARBOR_PASSWORD" }}
  
releases:
- name: yesodot-service
  namespace: {}
  chart: yesodot/common
  version: {{ requiredEnv "COMMON_VERSION" | default "0.5.2" }}
  values:
    - ./values.yaml

helmDefaults:
  recreatePods: true
  createNamespace: true
"""


values = """
name: {}
# If you want to overide the full name you can include the 'fullnameOverride' value
#fullname:
replicaCount: 1

images:
  PullSecrets: {}
  repository: {}
  tag: "latest"

config:name: "testname"
# If you want to overide the full name you can include the 'fullnameOverride' value
#fullname:
replicaCount: 1

images:
  PullSecrets: ['rabazhub']
  repository: rabazhub.azurecr.io/values-test
  tag: "latest"

config:
  configmaps: []
  env:
  - name: MESSAGE
    value: 'did work'

service:
  type: ClusterIP
  ports:
  - name: testname
    port: 3000
  - name: http
    port: 80
    protocol: TCP
  - name: https
    port: 443
    targetPort: 443

ingress:
  enabled: true
  hosts:
  - host: test-cd.branch-yesodot.org
    paths:
      - path: /message
        service: testname
        port: "3000"
  - name: {}
    port: 3000
  - name: http
    port: 80
    protocol: TCP
  - name: https
    port: 443
    targetPort: 443

ingress:
  enabled: {}
  hosts:
  - host: test-cd.branch-yesodot.org
    paths:
      - path: /message
        service: testname
        port: "3000"
"""

# name = 
# ingress = 
# pullsecret = 
# repository = 
# namespace = 

# @click.command()
# @click.argument('namespace', prompt='Your namespace.', default='guest')

# @click.argument('--ingress', prompt='ingress :true or false.', default='guest')

# @click.argument('--pullsecret', prompt='Your pullsecret.', default='guest')

# @click.argument('--repositiry', prompt='Your repository.', default='guest')

# @click.argument('--name', prompt='Your service name.', default='guest')


@click.command()
@click.option('--name', prompt='Your name',
              help='The person to greet.')
@click.option('--namespace', prompt='Your namespace',
              help='The person to greet.')
@click.option('--ingress', prompt='ingress: true or false',
              help='The person to greet.')
@click.option('--repo', prompt='Your repository',
              help='The person to greet.')
@click.option('--pullsecret', prompt='Your pullsecret',
              help='The person to greet.')

def hello(namespace , name, ingress, pullsecret, repo):
    print (helmfile.format(namespace))
    print (values.format(name, pullsecret,repo,name,ingress))
    file = open("values.yaml","w+")
    docs = yaml.load(values.format(name, pullsecret,repo,name,ingress))
    yaml.dump(docs, file, sort_keys=False)
    helmFile = open("helmfile.yaml","w+")
    docs = yaml.load(helmfile.format(namespace))
    yaml.dump(docs, helmFile, sort_keys=False)





if __name__ == '__main__':
    hello()