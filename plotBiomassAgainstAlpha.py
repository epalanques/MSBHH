#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:19:05 2018
@author: Romain GUEDON
Compare the value of the biomass of a model with another pre-selected model
"""

from fusion import *
from changerFluxes import *
import matplotlib.pyplot as plt
from cobra import *
from cobra.util.solver import linear_reaction_coefficients as linReaCoeff
import pandas as pd
import cobra.test

mini=cobra.test.create_test_model("mini")
model1=cobra.io.read_sbml_model("./Models/Bacteroides_sp_1_1_14.xml")
model2=cobra.io.read_sbml_model("./Models/Actinomyces_georgiae_DSM_6843.xml")

main(mini,mini,"vegan_diet.xls",2)

def main(oldModel1,oldModel2,diet,nbPoints=2):
    '''
    oldModel1,oldModel2 : two cobra.Model object
    diet: path of the file diet.xml containing the diet
    resolution: number of points 
    '''
    alphaList=[k/(nbPoints-1) for k in range(nbPoints)]#distributed btw 0 & 1
    biomass1List=[]#will contain biomass values of model1
    biomass2List=[]
    model1=oldModel1.copy()
    model2=oldModel2.copy()
    #On récupère les réactions de biomasses et on modifie le nom comme dans l'algo de fusion:
    ObjReac1=getBiomassReaction(model1)#ObjReac1 is a cobra reaction
    ObjReac2=getBiomassReaction(model2)
    objectiveTransformation(ObjReac1,"test")
    objectiveTransformation(ObjReac2,"test2")
    print(ObjReac1.metabolites)
    fusionModel=fusion([model1,model2])  
    print(ObjReac1.metabolites)
    #set the diet for each models:
    changerFluxes(diet,fusionModel)
    #Compute optimal biomass value for the given diet:
    optBiomass1=getOptimalBiomass(diet,model1)
    optBiomass2=getOptimalBiomass(diet,model2)
    #Proceed computation:
    for alpha in alphaList:
        objectiveModification(fusionModel,ObjReac1,ObjReac2,optBiomass1,optBiomass2,alpha)
        opt=fusionModel.optimize()
        biomass1List.append(opt.fluxes[ObjReac1.id+"_0"]/optBiomass1) #index added due to
        #name modification
        biomass2List.append(opt.fluxes[ObjReac2.id+"_1"]/optBiomass2)
    #Affichage
    AffichagePropre(alphaList,biomass1List,biomass2List,model1,model2)
    
def getOptimalBiomass(diet,model):    
    changerFluxes(diet,model)
    return model.optimize().f

def objectiveTransformation(ObjReac,indice):
    reactionNameChange(ObjReac,indice)
    for metab in ObjReac.metabolites:
        metaboliteNameChange(metab,indice)
        

def objectiveModification(fusionModel,ObjectiveReac1,ObjectiveReac2,optBiomass1,optBiomass2,alpha):
    '''
    fusionModel: the objective of fusionModel will be set as: alpha*Objective1 + 
    (1-alpha)*Objective2 
    Objective1, Objective2 : Cobra Reaction : it should be biomass reactions
    alpha: float 
    return an objective for a cobra model
    '''
    objectiveFusion=dict()
    objectiveFusion[ObjectiveReac1]=alpha/optBiomass1
    objectiveFusion[ObjectiveReac2]=(1-alpha)/optBiomass2
    fusionModel.objective=objectiveFusion
    print("\n Expression de l'objectif: \n ")
    print(fusionModel.objective.expression)
    print("\n Expression de la biomass1: \n")
    print(ObjectiveReac1.id)
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
    plt.figure()
    plt.plot(alphaList,biomass1List, label="biomass of model 1 ("+nameModel1+")",marker='x')
    plt.plot(alphaList,biomass2List, label = "biomass of model 2 ("+nameModel2+")",marker='x')
    title='''Biomass of each organism against alpha when the objective is : 
    alpha*biomassModel1 + (1-alpha)*biomassModel2 with '''+repr(len(alphaList))+" points"
    plt.title(title)
    plt.ylabel("biomass")
    plt.xlabel("alpha")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0.)
    


    
def TestOnModelsIJ(i,j):
    ListOfModels= pd.read_csv("./Models/listofmodel.txt", sep="\n", header=None).get_values()
    model1Name="./Models/"+ListOfModels[i][0]
    model2Name="./Models/"+ListOfModels[j][0]
    model1=cobra.io.read_sbml_model(model1Name)
    model2=cobra.io.read_sbml_model(model2Name)
    main(model1,model2,"vegan_diet.xls",2)
    



# =============================================================================
# print("Test de l'inversion model1/model2: ")
# model1Name="./Models/"+ListOfModels[0][0]
# model2Name="./Models/"+ListOfModels[1][0]
# model1=cobra.io.read_sbml_model(model1Name)
# model2=cobra.io.read_sbml_model(model2Name)
# main(model1,model2,"vegan_diet.xls",2)
# main(model2,model1,"vegan_diet.xls",2)
# =============================================================================
