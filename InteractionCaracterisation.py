#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:38:31 2018

@author: grom
"""

from minSharedReactions import *
from cobra import *
from plotBiomassAgainstAlpha import *
import matplotlib.pyplot as plt
from minSharedReactions import *
import time

#%%
def caracterisation(model1,model2,threshold):
    '''
        model1,2 : 2 cobra models
        threshold: integer = number min of shared reactions
    '''
    if compareReactions(model1,model2,threshold):
        plot(model1,model2)
        
    else:
        print("The number of reactions shared is lower than the fixed threshold")
        
 
ListOfDiets= pd.read_csv("./Diets/listOfDiets.txt", header = None, sep="\n").get_values()   
    

def plot(model1,model2):
    '''
    oldModel1,oldModel2 : two cobra.Model object 
    '''
    nameOfDiets=[]
    biomass1List=[]
    biomass2List=[]
    numDiet=0
    for numDiet in range(len(ListOfDiets)):
        diet="./Diets/"+ListOfDiets[numDiet][0]
        nameOfDiets.append(ListOfDiets[numDiet][0][:-4])
        fusionModel=fusion([model1,model2])  
        #Get the good biomass reactions:
        biomassReactions=getBiomassReactionV2(fusionModel)
        biomassReac1=biomassReactions[0]
        biomassReac2=biomassReactions[1]
        #set the diet 
        changerFluxes(diet,fusionModel)
        #Compute optimal biomass value for the given diet:
        optBiomass1=getOptimalBiomass(diet,model1)
        optBiomass2=getOptimalBiomass(diet,model2)
        #Change the objective
        objectiveModification(fusionModel,biomassReac1,biomassReac2,optBiomass1,optBiomass2,0.5)
        opt=fusionModel.optimize()
        biomass1List.append(opt.fluxes[biomassReac1.id]/optBiomass1)
        biomass2List.append(opt.fluxes[biomassReac2.id]/optBiomass2)
        
    #plot
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
    plt.scatter(nameOfDiets,biomass1List, label="biomass relative of model 1 \n("+nameModel1+")",marker='x',color='r')
    plt.scatter(nameOfDiets,biomass2List, label="biomass relative of model 2 \n("+nameModel2+")",marker='x',color='b')
    plotLine(0.5, nameOfDiets)
    plt.title("Biomasse relative des organismes en fonction de la diète")
    plt.ylabel("Biomasse relative")
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(0.5, -0.4), loc=8, borderaxespad=0.)
    plt.show()
    
def plotLine(h, d):
    plt.plot((min(d), max(d)), (0.5, 0.5), 'k:', label = None)

    
#%%
def TestSurIJCarac(i,j):
    s = time.time()
    ListOfModels= pd.read_csv("./Models/listofmodel.txt", sep="\n", header=None).get_values()
    ListOfDiets= pd.read_csv("./Diets/listOfDiets.txt", header = None, sep="\n").get_values()
    model1Name="./Models/"+ListOfModels[i][0]
    model2Name="./Models/"+ListOfModels[j][0] 
    model1=cobra.io.read_sbml_model(model1Name)
    model2=cobra.io.read_sbml_model(model2Name)
    print("------TEST------- \nmodèle 1 = "+ListOfModels[i][0][:-4]+" et modèle 2 = "+ListOfModels[j][0][:-4])
    print(round(time.time() - s, 2))
    s = time.time()
    caracterisation(model1,model2,2)
    print(round(time.time() - s, 2))
TestSurIJCarac(5,6)

