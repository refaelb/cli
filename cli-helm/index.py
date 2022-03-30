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
def writhBlockValues(imagename, replicacount, pullsecret, repo, tag ,configmap):
    with open(imagename+'-values.yaml', 'w') as yfile:
        yfile.write(values.format(imagename, replicacount, pullsecret, repo, tag ,configmap))

def serviceWriteStatic(dataservice, imagename):
    with open(imagename+'-values.yaml', 'a') as yfile:
        yfile.write(dataservice)

def serviceCountFunc (imagename, counts):
    for i in range(counts):
      questions = [
      inquirer.Text("name", message="service name",default="http"),
      inquirer.Text("port", message="service port" ,default=80)]
      answers = inquirer.prompt(questions)
      name = answers['name']
      port = answers['port']
      with open(imagename+'-values.yaml', 'a') as yfile:
        yfile.write(dataService.format(name, port))

def writeIngerssBlock1(imagename, ingress):
    if ingress == True:
        questions = [
        inquirer.Text("ingresshost", message="host to ingress " ),
    ]        
        answers = inquirer.prompt(questions)
        ingressHost = answers['ingresshost']
    else:
        ingress = False
        ingressHost = "nun"
    with open(imagename+'-values.yaml', 'a') as yfile:
        yfile.write(ingressBlock.format(ingress, ingressHost))

def writeIngressBlock2(imagename, dataingress,numberpath):
    for i in range (numberpath):
      questions = [
      inquirer.Text("ingresspath", message="path to ingress " ,default="/"),
      inquirer.Text("ingressport", message="port to ingress ", default=3000 ),
      inquirer.Text("ingressservice", message="service to ingress " )
      ]        
      answers = inquirer.prompt(questions)
      ingresspath = answers['ingresspath']
      ingressport = answers['ingressport']
      ingressservice = answers['ingressservice']
      with open(imagename+'-values.yaml', 'a') as yfile:
          yfile.write(dataingress.format(ingresspath, ingressservice, ingressport))



@click.command()
@click.option('--imagename', prompt='Your service name',help='The person to greet.')
# @click.option('--namespace', prompt='Your namespace',help='The person to greet.')
@click.option('--replicacount',default=1, prompt='count replica ',help='The person to greet.')
@click.option('--pullsecret', prompt='Your pullsecret',help='The person to greet.')
@click.option('--repo', prompt='Your repository',help='The person to greet.')
@click.option('--tag', default="latest",prompt='tag to service',help='The person to greet.')
@click.option('--configmap',default=[], prompt='Your configmap',help='The person to greet.')
###service###
# @click.echo('service configure')
@click.option('--counts',default=1, prompt='counts service',help='The person to greet.')
###ingress###
# @click.echo('ingres configure')
@click.option('--ingress', default=False, prompt='###ingress### \ningress: true or false',help='The person to greet.')
@click.option('--numberpath',default=1,  prompt='number path ',help='The person to greet.')


def main(imagename, replicacount, pullsecret, repo, tag ,configmap, ingress,counts,numberpath):
    writhBlockValues(imagename, replicacount, pullsecret, repo, tag ,configmap)
    serviceWriteStatic(dataservice,imagename)
    serviceCountFunc(imagename, counts)
    writeIngerssBlock1(imagename, ingress)
    writeIngressBlock2(imagename, dataingress, numberpath)


if __name__ == '__main__':
    main()
    ()