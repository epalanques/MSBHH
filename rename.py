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

def compareaction(model1, model2, seuil):
  #seuil est une nombre de réactions minimales communes pour qu'on puisse considérer que les deux modèles peuvent interagir et méritent une étude plus approfondie
    listecommune=[]
    nb_reactions_communes=0
    for i in range (len(reactionex(model1)[0])):
        if reactionex(model1)[0][i] in reactionex(model2)[0]:
            listecommune.append(reactionex(model1)[0][i])
            nb_reactions_communes+=1
    if nb_reactions_communes >= seuil :
      return True #les deux modèles peuvent interagir et leur interaction vaut la peine d'être étudiée
    else: 
      return False #le nombre de reactions communes aux 2 modèles est trop faible, on n'étudie donc pas leur comparaison
    
