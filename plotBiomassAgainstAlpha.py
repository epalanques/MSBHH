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
from cobra.util.solver import linear_reaction_coefficients as linReaCoeff

import cobra.test
mini=cobra.test.create_test_model("mini")

def main(model1,model2,diet,resolution):
    '''
    model1,model2 : two cobra.Model object
    diet: name of the file containing the diet
    resolution: number of points (minus one)
    '''
    alphaList=[k/resolution for k in range(resolution+1)]
    biomassList=[]
    fusionModel=fusion([model1,model2])
    #changerFluxes(diet,fusionModel)
    #biomass2List=[]
    
    #Get the biomass reactions by this way:
    ObjectiveReactionsModel1=linReaCoeff(model1)
    for item in ObjectiveReactionsModel1.keys():
        ObjReac=item
#    for value in ObjectiveReactionsModel1.values():
#        ObjValue=value
        
    for alpha in alphaList:
        fusionModel.objective= alpha*model1.objective.expression + (1-alpha)*model2.objective.expression
        print(fusionModel.objective.expression)
        opt=fusionModel.optimize()
        biomassList.append(opt.fluxes[ObjReac.id+"_0"])# Adding "_0" because of the fusion that renammed the reactions with the index 0 for the model1 (index)
        
    #plt.plot(alphaList,biomassList)
    return(biomassList[0])

#dict1=dict({"Key1" : "Value1"})
#print(dict1.__getitem__("Key1"))

#mini=changerFluxes("vegan_diet.xls",mini)
optmini=mini.optimize()
print(optmini.fluxes.keys())
main(mini,mini,"vegan_diet.xls",4)



model1=cobra.io.read_sbml_model("./Models/Bacteroides_sp_1_1_14.xml")
model2=cobra.io.read_sbml_model("./Models/Bacteroides_fragilis_3_1_12.xml")
main(model1,model2,"vegan_diet.xls",1)

#TEST##

model1=cobra.io.read_sbml_model("./Models/Bacteroides_sp_1_1_14.xml")
ObjectiveReactionsModel1=linReaCoeff(model1)
for item in ObjectiveReactionsModel1.keys():
    ObjReac=item
ObjReac
opt1=model1.optimize()
opt1.fluxes[ObjReac.id]


