import cobra
import cobra.test
import os
from os.path import join
import pandas
import difflib
import xlsxwriter

def reactionex(model):
  l=[]
  count=0
  for rec in model.reactions: 
    if rec.id.startswith("EX"): 
      l.append((rec.id, rec.reaction,rec.name))
      count+=1
  return (l,count)
      
def rename_1(model):
  for rec in model.metabolites:
    rec.id=rec.id+"_1"
  return model
  
def rename_2(model):
  for rec in model.metabolites:
    rec.id=rec.id+"_2"
  return model

def compareaction(model1, model2):
    listecommune=[]
    count=0
    for i in range (len(reactionex(model1)[0])):
        if reactionex(model1)[0][i] in reactionex(model2)[0]:
            listecommune.append(reactionex(model1)[0][i])
            count+=1
    return ("Les modèles "+str(model1.id)+" et "+str(model2.id)+" partagent "+str(count)+" réactions d'échange avec l'extérieur : "+str(listecommune))

