#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:19:05 2018
@author: Romain GUEDON
Compare the value of the biomass of a model with another pre-selected model
"""
#%% Importations

from fusion import *
from main1 import *
import matplotlib.pyplot as plt
from cobra import *
from cobra.util.solver import linear_reaction_coefficients as linReaCoeff
import pandas as pd
import cobra.test

#%% 
def main(model1,model2,diet,nbPoints=2):
    '''
    oldModel1,oldModel2 : two cobra.Model object
    diet: path of the file diet.xml containing the diet
    nbPoints: number of points 
    '''
    alphaList=[k/(nbPoints-1) for k in range(nbPoints)]#distributed btw 0 & 1
    biomass1List=[]#will contain biomass values of model1
    biomass2List=[]
    fusionModel=fusion([model1,model2])  
    #Get the good biomass reactions:
    biomassReactions=getBiomassReactionV2(fusionModel)
    biomassReac1=biomassReactions[0]
    biomassReac2=biomassReactions[1]
#    print(biomassReac2.id)
#    print(model2.objective)
    #set the diet 
    changerFluxes(diet,fusionModel)
    #Compute optimal biomass value for the given diet:
    optBiomass1=getOptimalBiomass(diet,model1)
    optBiomass2=getOptimalBiomass(diet,model2)
    #Proceed computation:
    for alpha in alphaList:
        objectiveModification(fusionModel,biomassReac1,biomassReac2,optBiomass1,optBiomass2,alpha)
#        print("The model's objective is :")
#        print(fusionModel.objective.expression)
        opt=fusionModel.optimize()
#        print(opt.fluxes[biomassReac1.id]/optBiomass1)
        biomass1List.append(opt.fluxes[biomassReac1.id]/optBiomass1)
        biomass2List.append(opt.fluxes[biomassReac2.id]/optBiomass2)
    #Affichage
    AffichagePropre(alphaList,biomass1List,biomass2List,model1,model2)
#%%
    
    
#%% Sub-functions
    
def getOptimalBiomass(diet,model):    
    model=changerFluxes(diet,model)
    return model.optimize().f

#def objectiveTransformation(ObjReac,indice):
#    reactionNameChange(ObjReac,indice)
#    for metab in ObjReac.metabolites:
#        metaboliteNameChange(metab,indice)
        

def objectiveModification(fusionModel,ObjectiveReac1,ObjectiveReac2,optBiomass1,optBiomass2,alpha):
    '''
    fusionModel: the objective of fusionModel will be set as: alpha/optBiomass1*Objective1 + 
    (1-alpha)/optBiomass2*Objective2 def plotLine(h, d):
    plt.plot((min(d), max(d)), (0.5, 0.5), 'k:', label = None)
    ObjectiveReac1, ObjectiveReac2 : Cobra Reaction : it should be the biomass reactions
    alpha: float (between 0 and 1) 
    '''
    temp = (alpha/optBiomass1)*ObjectiveReac1.flux_expression + ((1-alpha)/optBiomass2)*ObjectiveReac2.flux_expression
    fusionModel.objective = fusionModel.problem.Objective(temp)

def plotLine2(h,alphaList):
    plt.plot(alphaList, [h for k in range(len(alphaList))], 'k:', label = None)

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
    plt.figure(figsize = (14,7))
    plt.plot(alphaList,biomass1List, label="biomass of model 1 ("+nameModel1+")",marker='x')
    plt.plot(alphaList,biomass2List, label = "biomass of model 2 ("+nameModel2+")",marker='x')
    plotLine2(1, alphaList)
    title='''Biomass of each organism against alpha when the objective is : 
    alpha*biomassModel1 + (1-alpha)*biomassModel2 with '''+repr(len(alphaList))+" points"
    plt.title(title)
    plt.ylabel("relative biomass")
    plt.xlabel("alpha")
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(0.5, -0.4), loc=8, borderaxespad=0.)
    plt.show()
    
#%% Test functions
    
def TestSurMini(nbPoints):
    mini=cobra.test.create_test_model("mini")
    main(mini,mini,"./Diets/Vegan.xls",nbPoints)
    


def TestOnModelsIJ(i,j,numDiet,nbPoints):
    '''
    On utilise une liste de modèle pour parcourir l'ensemble des modèles du répertoire /Models
    La fonction exécute un test du plot sur la diète vegan (la meilleure)
    '''
    ListOfModels= pd.read_csv("./Models/listofmodel.txt", sep="\n", header=None).get_values()
    ListOfDiets= pd.read_csv("./Diets/listOfDiets.txt", header = None, sep="\n").get_values()
    diet="./Diets/"+ListOfDiets[numDiet][0]
    model1Name="./Models/"+ListOfModels[i][0]
    model2Name="./Models/"+ListOfModels[j][0] 
    model1=cobra.io.read_sbml_model(model1Name)
    model2=cobra.io.read_sbml_model(model2Name)
    print("------TEST------- \nmodèle 1 = "+ListOfModels[i][0][:-4]+" et modèle 2 = "+ListOfModels[j][0][:-4]+" avec la diète "
          +ListOfDiets[numDiet][0][:-4])
    main(model1,model2,diet,nbPoints)
    
def Test_Ecoli_Salmo(numDiet,nbPoints):
    model1=cobra.test.create_test_model("salmonella")
    model1.name="Salmonelle"
    model2=cobra.test.create_test_model("ecoli")
    model2.name="Esherichia Coli"
    diet="./Diets/"+ListOfDiets[numDiet][0]
    print("------TEST------- \nmodèle 1 = Salmonelle et modèle 2 = Esherichia Coli avec la diète "
          +ListOfDiets[numDiet][0][:-4])
    main(model1,model2,diet,nbPoints)
    
    
#%% Tests

#Inversion of 2 models in the function: 
    
#TestOnModelsIJ(8,7,7,15)
#TestOnModelsIJ(5,6,7,15)

Test_Ecoli_Salmo(1,10)



