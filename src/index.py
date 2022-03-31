from random import choices
import click
import inquirer

values = """
name: {}
#fullname:
replicacounts: {}

images:
  PullSecrets: 
  - {}
  repository: {}
  tag: {}

config:
  configmaps: {}
"""

dataservice="""
service:
  type: ClusterIP
  ports: """

dataService = """
  - name: {}
    port: {}
    """

ingressBlock = """
ingress:
  enabled: {}
  hosts:
  - host: {}
    paths: """

dataingress = """
    - path: {}
      service: {}
      port: {}
"""


helmFile = """
environments:
  dev:
  prod:
repositories:
- name: yesodot
  url: https://harborreg-2.northeurope.cloudapp.azure.com/chartrepo/library
  username: {{ requiredEnv "HARBOR_USER" }}
  password: {{ requiredEnv "HARBOR_PASSWORD" }}
  
releases:
- name: {}
  namespace: {}
  chart: yesodot/common
  version: {{ requiredEnv "COMMON_VERSION" | default "0.5.2" }}
  values:
    - ./values.yaml
helmDefaults:
  recreatePods: true
  createNamespace: {}
"""



def writhBlockValues(imagename, replicacount, pullsecret, repo, tag ,configmap):
    with open(imagename+'-values.yaml', 'w') as yfile:
        yfile.write(values.format(imagename, replicacount, pullsecret, repo, tag ,configmap))

def serviceWriteStatic(dataservice, imagename):
    with open(imagename+'-values.yaml', 'a') as yfile:
        yfile.write(dataservice)

def serviceCountFunc (imagename, counts):
    for i in range(counts):
      questions = [
      inquirer.Text("name", message="service {0} name".format(i + 1),default="http  "),
      inquirer.Text("port", message="service {0} port".format(i + 1) ,default=80)]
      answers = inquirer.prompt(questions)
      name = answers['name']
      port = answers['port']
      with open(imagename+'-values.yaml', 'a') as yfile:
        yfile.write(dataService.format(name, port))

def writeIngerssBlock1(imagename, ingress):
    if ingress == True:
        questions = [
        inquirer.Text("numberPath", message="number of path ", default=1 ),
        inquirer.Text("ingresshost", message="host to ingress " ),
    ]        
        answers = inquirer.prompt(questions)
        ingressHost = answers['ingresshost']
        numberPath = answers['numberPath']
    else:
        ingress = False
        ingressHost = "'nun'"
        numberPath = 1
    with open(imagename+'-values.yaml', 'a') as yfile:
        yfile.write(ingressBlock.format(ingress, ingressHost))
    writeIngressBlock2(imagename, dataingress, numberPath)

def writeIngressBlock2(imagename, dataingress,numberPath):
    for i in range (numberPath):
      questions = [
      inquirer.Text("ingresspath", message="path no. {0} to ingress".format(i + 1) ,default="/"),
      inquirer.Text("ingressport", message="port to ingress path no. {0}".format(i + 1) , default=3000 ),
      inquirer.Text("ingressservice", message="service to ingress path no. {0}".format(i + 1) )
      ]        
      answers = inquirer.prompt(questions)
      ingresspath = answers['ingresspath']
      ingressport = answers['ingressport']
      ingressservice = answers['ingressservice']
      with open(imagename+'-values.yaml', 'a') as yfile:
          yfile.write(dataingress.format(ingresspath, ingressservice, ingressport))

def createHelmFile(imagename, helmFile):
    questions = [
    inquirer.Text("namespace", message="your namespace " , default='default'),
    inquirer.Text('createNamespace', message="create namespace",choices=['true', 'false'], default='False'),
    ]        
    answers = inquirer.prompt(questions)
    namespace = answers['namespace']
    createNamespace = answers['createNamespace']
    with open(imagename+'-helmfile.yaml', 'w') as yfile:
        yfile.write(helmFile.format(imagename, namespace, createNamespace))

@click.command()
@click.option('--imagename', prompt='Your service name',help='The person to greet.')
@click.option('--replicacount',default=1, prompt='replica count ',help='The person to greet.')
@click.option('--pullsecret', prompt='Your pullsecret',help='The person to greet.')
@click.option('--repo', prompt='Your repository (image without tag)',help='The person to greet.')
@click.option('--tag', default="latest",prompt='Your image\'s tag',help='The person to greet.')
@click.option('--configmap',default=[], prompt='Your configmap(s)',help='The person to greet.')
###service###
@click.option('--counts',default=1, prompt='number of k8s services',help='The person to greet.')
###ingress###
@click.option('--ingress', default=False, prompt='###ingress### \ningress: true or false',help='The person to greet.')


def main(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress,counts):
    writhBlockValues(imagename, replicacount, pullsecret, repo, tag ,configmap)
    serviceWriteStatic(dataservice,imagename)
    serviceCountFunc(imagename, counts)
    writeIngerssBlock1(imagename, ingress)
    createHelmFile(imagename, helmFile)


if __name__ == '__main__':
    main()
    ()