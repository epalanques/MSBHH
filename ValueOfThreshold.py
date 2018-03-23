#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:40:44 2018

@author: grom
"""

from cobra import *
import main1
from plotBiomassAgainstAlpha import *
#%%
def ValueOfThreshold(model,percentOfMean):

    ListOfDiets= pd.read_csv("./Diets/listOfDiets.txt", header = None, sep="\n").get_values()
    biomass=0
    for numDiet in range(len(ListOfDiets)):
        diet="./Diets/"+ListOfDiets[numDiet][0]
        biomass+=getOptimalBiomass(diet,model)
    biomass/=len(ListOfDiets)
    
#%%
