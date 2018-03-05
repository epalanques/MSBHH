#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:19:05 2018

@author: Romain GUEDON

Compare the value of the biomass of a model with another pre-selected model
"""

from fusion import fusion 
from changerFluxes import changerFluxes
import matplotlib.pyplot as plt
from cobra import Model, Reaction, Metabolite

def main(model1,model2,diet,resolution):
    '''
    model1,model2 : two cobra.Model object
    diet: name of the file containing the diet
    resolution: number of points (minus one)
    '''
    alphaList=[k/resolution for k in range(resolution+1)]
    biomassList=[]
    fusionModel=fusion([model1,model2])
    #biomass2List=[]
    for alpha in alphaList:
        
        fusionModel.objective= alpha*model1.objective.expression + (1-alpha)*model2.objective.expression
        print(fusionModel.optimize())
        changerFluxes(diet,fusionModel)
        fusionModel.optimize()
        #biomass1= IL FAUT RETROUVER LA VALEUR DE LA BIOMASS1
        
        
    #plt.plot(alphaList,biomass1List)

main(mini,mini,"vegan_diet.xls",1)



model1=cobra.io.read_sbml_model("./Models/Bacteroides_sp_1_1_14.xml")
model2=cobra.io.read_sbml_model("./Models/Bacteroides_fragilis_3_1_12.xml")





