import cobra
import cobra.test
import os
from os.path import join
import pandas
import difflib
import xlsxwriter

def reactionex(model):
  l=[]
  for rec in model.reactions: 
    if rec.id.startswith("EX"): 
      l.append((rec.id, rec.reaction,rec.name))
  return l
      
def rename_1(model):
  for rec in model.metabolites:
    rec.id=rec.id+"_1"
  return model
  
def rename_2(model):
  for rec in model.metabolites:
    rec.id=rec.id+"_2"
  return model
