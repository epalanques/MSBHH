#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 19:20:36 2018
@author: Romain GUEDON
"""
import cobra.test
from cobra import Model, Reaction, Metabolite
from cobra.util.solver import linear_reaction_coefficients as linReaCoeff

def getBiomassReaction(model):
    objReactions=linReaCoeff(model)
    for item in objReactions:#works with only one biomass reaction !
        reac=item
    return reac

def getBiomassReactionV2(model):
    reac=Reaction()
    objReactions=linReaCoeff(model)
    for item in objReactions:#works with only one biomass reaction !
        reac=item
    return reac

def finderOfEX(model):
    '''
    Return a dictList of cobra reactions starting with EX
    '''
    res=[]
    for x in model.reactions:
        if type(x.id)==type("string") and x.id.startswith("EX"): 
            res.append(x.id)
    return res

def nameChange(NewModel,indice):
    '''
        Change the model with Name, Metabolites and Reactions  
        renamed with the indice! (Genes are not)
        
        indice: integer
        NewModel: cobra.Model
    '''
    indice=str(indice)
    if type(NewModel.name)==type("string"):
        NewModel.name=NewModel.name+"_"+indice
    else:
        NewModel.name="ModelWithoutName"+indice
    for reac in NewModel.reactions:
        reactionNameChange(reac,indice)
    for metab in NewModel.metabolites:
        metaboliteNameChange(metab,indice)
    

def reactionNameChange(reac,indice):
    reac.id=reac.id+"_"+indice
    if type(reac.name)==type("string"):
        reac.name=reac.name+"_"+indice
    if type(reac.subsystem)==type("string"):
        reac.subsystem=reac.subsystem+"_"+indice

def metaboliteNameChange(metab,indice):
    metab.id=metab.id+"_"+indice
    if type(metab.name)==type("string"):
        metab.name=metab.name+"_"+indice
    if type(metab.compartment)==type("string"):
        metab.compartment=metab.compartment+"_"+indice    


def fusion(oldModelList):
    '''
    --Parameters--
    modelList est une liste de modèles. En pratique de longueur 2 ou 3
    
    --Return--
    Return the fusion of the models 
    '''
    #Initialisation
    NewModel = cobra.Model("Fusion des modèles !")
    modelList=[]
    for old in oldModelList:
        modelList.append(old.copy())
    #Change Name and add reactions (and metabolites, genes...) in the NewModel
    i=0
    for model in modelList:
        nameChange(model,i)
        NewModel.add_reactions(model.copy().reactions)
        i+=1

    #Modification des réactions EX comme décrit:
    EX_ReactionsModif=[]
    for model in modelList:#On récupère des réactions modifiées
        EX_ReactionsModif+=finderOfEX(model)
    
    
    for idEX in EX_ReactionsModif:
        rootReac = NewModel.reactions.get_by_id(idEX)#Reaction avec une seule métabolite que l'on récupère:
        for metab in rootReac.metabolites:#Un seul métabolite #utilisation boucle car difficultés à récupérer autrement
            rootMetab = NewModel.metabolites.get_by_id(metab.id)
            #Il ne faut pas mettre l'indice ajouté précédemment par le changement de nom
            #dans la nouvelle métabolite:
            rootMetabtemp=rootMetab.copy()
            rootMetabtemp.id=rootMetabtemp.id[:-2]#on avait ajouté "_i"
            rootMetabtemp.name=rootMetabtemp.name[:-2]
            poolMetab = Metabolite(
                'pool_'+rootMetabtemp.id,
                formula=rootMetabtemp.formula,
                compartment='pool',
                name='Version pool de '+rootMetabtemp.name
            )
            rootReac.add_metabolites({ ##
                poolMetab : -rootMetabtemp.charge #charge = coefficient stoechiometrique de root dans la reaction i.e. -1 normalement
            })
        #Ajout des réaction "pool_xxx_e <-> " que l'on identifient par "pool_xxx"
        #RQ: si la réaction existe déjà, cobrapy ne l'ajoute pas deux fois donc pas de soucis de doublons.
        poolReac = Reaction('pool_'+rootMetabtemp.id)
        poolReac.name='Reaction controle : '+rootMetabtemp.id+'_pool <->'
        poolReac.subsystem = 'pool'
        poolReac.lower_bound=-1000
        poolReac.upper_bound=1000
        poolReac.add_metabolites({
            poolMetab : -1.0
        })
        if not(poolReac in NewModel.reactions):
            NewModel.add_reactions([poolReac])
    #Objective modification
    ObjReacList=dict()
    j=0
    for model in modelList:
        BiomassReac=getBiomassReaction(model)#Return only one of several reactions in model objective
        ObjReacList[BiomassReac]=1.0
        j+=1
    NewModel.objective=ObjReacList
    return NewModel

model1=cobra.io.read_sbml_model("./Models/Actinomyces_georgiae_DSM_6843.xml")
fusion([model1,model1])
mini=cobra.test.create_test_model("mini")
fusionModel=fusion([model1,mini])
fusionModel.objective.expression
model1.objective.expression
mini.objective.expression

def Validation(mini,reaction):
    print("Expression de l'objectif au début: ")
    print(mini.objective.expression)
    linReaResult=linReaCoeff(mini)
    print("le résultat de linReaCoeff est : ")
    print(linReaResult)
    linReaResult[reaction]=1.0
    print("Après modif, linReaCoeff est : ")
    print(linReaResult)
    mini.objective=linReaResult
    print("Expression de l'objectif après modif de linReaResult: ")
    print(mini.objective.expression)
    
    
def Validation2(oldmodel):
    print("linRea du vieux")  
    print(linReaCoeff(oldmodel))
    model=oldmodel.copy()
    print("linRea du nouveau")  
    print(linReaCoeff(model))
    nameChange(model,0)
    print("linRea du nouveau après nameChange")  
    print(linReaCoeff(model))   
    
def Validation3():
    print(model1.objective.expression)
    print(mini.objective.expression)
    print(fusion([mini,model1]).objective.expression)
    