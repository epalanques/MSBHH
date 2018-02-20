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
      
def rename(model):
  
