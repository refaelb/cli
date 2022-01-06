import click

def writeConfig(**kwargs):
    values = """
name: {name}
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
  ports:
  - name: {servicename}
    port: {port}
  - name: http
    port: 80
    protocol: TCP
  - name: https
    port: 443
    targetPort: 443

ingress:
  enabled: {ingress}
  hosts:
  - host: {host}
    paths:
      - path: {peth}
        service: {servicename}
        port: {port}
    """
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
- name: {servicename}
  namespace: {namespace}
  chart: yesodot/common
  version: {{ requiredEnv "COMMON_VERSION" | default "0.5.2" }}
  values:
    - ./values.yaml

helmDefaults:
  recreatePods: true
  createNamespace: true
    """
    with open('values.yaml', 'w') as yfile:
        yfile.write(values.format(**kwargs))

    with open('helmfile.yaml', 'w') as yfile:
        yfile.write(helmfile.format(**kwargs))

@click.command()
@click.option('--name', prompt='Your name',help='The person to greet.')
@click.option('--namespace', prompt='Your namespace',help='The person to greet.')
@click.option('--replicacount',default=1, prompt='replicacount',help='The person to greet.')
@click.option('--pullsecret', prompt='Your pullsecret',help='The person to greet.')
@click.option('--repo', prompt='Your repository',help='The person to greet.')
@click.option('--tag', default="latest",prompt='tag',help='The person to greet.')
@click.option('--configmap',default=[], prompt='Your configmap',help='The person to greet.')
@click.option('--servicename', prompt='servicename',help='The person to greet.')
@click.option('--port', default=3000,prompt='port',help='The person to greet.')
@click.option('--ingress', default=False, prompt='ingress: true or false',help='The person to greet.')
@click.option('--peth', default="nun",prompt='Your peth',help='The person to greet.')
@click.option('--host', default="nun",prompt='host',help='The person to greet.')

def hello(name,namespace,replicacount,pullsecret,repo,tag,configmap,servicename,port,ingress,host,peth):
      print(name,namespace,replicacount,pullsecret,repo,tag,configmap,servicename,port,ingress,host,peth)
      writeConfig(name=name,replicacount=replicacount,pullsecret=pullsecret, repo=repo, tag=tag,configmap=configmap,servicename=servicename, port=port, ingress=ingress ,host=host,peth=peth, namespace=namespace)

hello()

# name = "refael"
# replicacount=1
# pullsecret=1
# repo=1
# tag=1
# configmap=1
# servicename=1
# port=1
# ingress=1
# peth=1
# host=1
    