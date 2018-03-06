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
import pandas as pd
import cobra.test
mini=cobra.test.create_test_model("mini")
model1=cobra.io.read_sbml_model("./Models/Bacteroides_sp_1_1_14.xml")
model2=cobra.io.read_sbml_model("./Models/Bacteroides_fragilis_3_1_12.xml")

def main(model1,model2,diet,resolution):
    '''
    model1,model2 : two cobra.Model object
    diet: name of the file containing the diet
    resolution: number of points (minus one)
    '''
    alphaList=[k/resolution for k in range(resolution+1)]
    biomass1List=[]
    biomass2List=[]
    ObjReac1=getBiomassReaction(model1)
    ObjReac2=getBiomassReaction(model2)
    fusionModel=fusion([model1,model2])
    #Proceed computation:
    for alpha in alphaList:
        objectiveModification(fusionModel,ObjReac1,ObjReac2,alpha)
        opt=fusionModel.optimize()
        biomass1List.append(opt.fluxes[ObjReac1.id+"_0"] #index added due to
        #name modification
        biomass2List.append(opt.fluxes[ObjReac2.id+"_1"])
    #Affichage
    AffichagePropre(alphaList,biomass1List,biomass2List,model1,model2)
    

def objectiveModification(fusionModel,ObjectiveReac1,ObjectiveReac2,alpha):
    '''
    fusionModel: the objective of fusionModel will be set as: alpha*Objective1 + 
    (1-alpha)*Objective2 
    Objective1, Objective2 : Cobra Reaction : it should be biomass reactions
    alpha: float 
    return an objective for a cobra model
    '''
    objectiveFusion=dict()
    objectiveFusion[ObjectiveReac1]=alpha 
    objectiveFusion[ObjectiveReac2]=1-alpha
    fusionModel.objective=objectiveFusion
    return fusionModel

def getBiomassReaction(model):
    objReactions=linReaCoeff(model)
    for item in objReactions:#works with only one biomass reaction !
        reac=item
    return(reac)


def AffichagePropre(alphaList,biomass1List,biomass2List,model1,model2):
    #Superficialité:
    if not(type(model1.name)==type("")):
        nameModel1="NoNamedmodel1"
    else:
        nameModel1=model1.name
    if not(type(model2.name)==type("")):
        nameModel2="NoNamedmodel2"
    else:
        nameModel2=model2.name
    
    plt.plot(alphaList,biomass1List, label="biomass of model 1 ("+nameModel1+")",marker='x')
    plt.plot(alphaList,biomass2List, label = "biomass of model 2 ("+nameModel2+")",marker='x')
    title='''Biomass of each organism against alpha when the objective is : 
    alpha*biomassModel1 + (1-alpha)*biomassModel2 with '''+repr(len(alphaList))+" points"
    plt.title(title)
    plt.ylabel("biomass")
    plt.xlabel("alpha")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0.)
main(mini,mini,"vegan_diet.xls",10)



