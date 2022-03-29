from cgi import print_arguments
from inspect import modulesbyfile
from tkinter.messagebox import QUESTION
from tokenize import Name
from unicodedata import name
import click
import yaml
import re
import inquirer




values = """
name: {}
#fullname:
replicacounts: {}

images:
  PullSecrets: {}
  repository: {}
  tag: {}

config:
  configmaps: {}
  env:
  - name: MESSAGE
    value: 'did work'

ingress:
  enabled: {}
  hosts:
  - host: {}
    paths:
      - path: {}
        service: {}
        port: {}
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
- name: {}
  namespace: {}
  chart: yesodot/common
  version: {{ requiredEnv "COMMON_VERSION" | default "0.5.2" }}
  values:
    - ./values.yaml

helmDefaults:
  recreatePods: true
  createNamespace: true
    """

dataService = """
service:
  type: ClusterIP
  ports:
  - name: {}
    port: {}
    """


@click.command()
@click.option('--imagename', prompt='Your service name',help='The person to greet.')
# @click.option('--namespace', prompt='Your namespace',help='The person to greet.')
@click.option('--replicacount',default=1, prompt='count replica ',help='The person to greet.')
@click.option('--pullsecret', prompt='Your pullsecret',help='The person to greet.')
@click.option('--repo', prompt='Your repository',help='The person to greet.')
@click.option('--tag', default="latest",prompt='tag to service',help='The person to greet.')
@click.option('--configmap',default=[], prompt='Your configmap',help='The person to greet.')
###service###
@click.option('--counts',default=1, prompt='counts service',help='The person to greet.')

###ingress###
@click.option('--ingress', default=False, prompt='###ingress### \ningress: true or false',help='The person to greet.')
# @click.option('--ingresspath', default="nun",prompt='Your peth in service to ingress',help='The person to greet.')
# @click.option('--ingressport', default=3000,prompt='port in service to ingress ',help='The person to greet.')
# @click.option('--ingresshost', default="nun",prompt='host to ingress',help='The person to greet.')
# @click.option('--ingressservice', default="nun",prompt='service name to ingress',help='The person to greet.')


def main(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress,counts):
    ingressfunc(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress,counts)

def ingressfunc(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress, counts):
    print (ingress)
    if ingress == True:
        questions = [
        inquirer.Text("ingresspath", message="path in service to ingress?"),
        inquirer.Text("ingressport", message="port in service to ingress " ),
        inquirer.Text("ingresshost", message="host to ingress " ),
        inquirer.Text("ingressservice", message="service name to ingress" )
    ]
        answers = inquirer.prompt(questions)
        ingresspath = answers['ingresspath']
        ingressport = answers['ingressport']
        ingresshost = answers['ingresshost']
        ingressservice = answers['ingressservice']
    else:
        ingress = False
        ingresspath = "nun"
        ingressport = "nun"
        ingresshost = "nun"
        ingressservice = "nun"
    # return ingress
    countfunc(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress, ingresshost, ingresspath, ingressservice, ingressport,counts)

def countfunc (imagename, replicacount, pullsecret, repo, tag ,configmap, ingress, ingresshost, ingresspath, ingressservice, ingressport, counts):
    write(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress, ingresshost, ingresspath, ingressservice, ingressport)
    for i in range(counts):
      questions = [
      inquirer.Text("name", message="service name"),
      inquirer.Text("port", message="service port" )
  ]
      answers = inquirer.prompt(questions)
      name = answers['name']
      port = answers['port']
      countService(imagename, name, port)

def countService(imagename, name, port):  
    with open(imagename+'-values.yaml', 'a') as yfile:
        yfile.write(dataService.format(name, port))

def write(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress, ingresshost, ingresspath, ingressservice, ingressport):
    with open(imagename+'-values.yaml', 'w') as yfile:
        yfile.write(values.format(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress, ingresshost, ingresspath, ingressservice, ingressport))
        # with open('helmfile.yaml', 'w') as yfile:
        #     yfile.write(helmfile.format(**kwargs))


if __name__ == '__main__':
    main()
    ()