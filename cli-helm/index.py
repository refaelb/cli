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

ingress:
  enabled: {}
  hosts:
  - host: {}
    paths:
      - path: {}
        service: {}
        port: {}

service:
  type: ClusterIP
  ports: """

dataService = """
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


def main(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress,counts):
    ingressfunc(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress)
    # write(imagename, replicacount, pullsecret, repo, tag ,configmap,ingress,myarray)
    countfunc(imagename, counts)

def ingressfunc( imagename, replicacount, pullsecret, repo, tag ,configmap, ingress):
    print (ingress)
    if ingress == True:
        questions = [
        inquirer.Text("ingresshost", message="host to ingress " ),
        inquirer.Text("ingresspath", message="path in service to ingress?"),
        inquirer.Text("ingressport", message="port in service to ingress " ),
        inquirer.Text("ingressservice", message="service name to ingress" )
    ]        
        answers = inquirer.prompt(questions)
        ingresshost = answers['ingresshost']
        ingresspath = answers['ingresspath']
        ingressport = answers['ingressport']
        ingressservice = answers['ingressservice']
    else:
        ingress = False
        ingresshost = "nun"
        ingresspath = "nun"
        ingressport = "nun"
        ingressservice = "nun"
    with open(imagename+'-values.yaml', 'w') as yfile:
        yfile.write(values.format(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress,ingresshost,ingresspath,ingressservice,ingressport))

        # return ingress , ingresshost, ingresspath, ingressport , ingressservice

def write(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress,myarray):
    with open(imagename+'-values.yaml', 'w') as yfile:
        ingresspath = myarray[1]
        ingressport = myarray[2]
        ingresshost = myarray[3]
        ingressservice = myarray[4]
        yfile.write(values.format(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress,ingresshost,ingresspath,ingressservice,ingressport))

def countfunc (imagename, counts):
    for i in range(counts):
      questions = [
      inquirer.Text("name", message="service name"),
      inquirer.Text("port", message="service port" )
  ]
      answers = inquirer.prompt(questions)
      name = answers['name']
      port = answers['port']
      with open(imagename+'-values.yaml', 'a') as yfile:
        yfile.write(dataService.format(name, port))


if __name__ == '__main__':
    main()
    ()