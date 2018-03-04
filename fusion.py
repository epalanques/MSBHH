#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 19:20:36 2018

@author: Romain GUEDON
"""
import cobra.test
mini=cobra.test.create_test_model("mini")

#Fonction principale
def fusion(OldModelList):
    '''
    --Parameters--

    modelList est une liste de modèles. En pratique de longueur 2 ou 3
    
    --Return--
    Return the fusion of the models 
    '''
#Sub-fonctions
    def nameChange(model,indice):
        '''
            Returns a copy of the model with Name, Metabolites and Reactions  
            renamed with the indice! (Genes are not)
        '''
        indice=str(indice)
        NewModel=model.copy()
        if type(NewModel.name)==type("string"):
            NewModel.name=NewModel.name+"_"+indice
        else:
            NewModel.name="ModelWithoutName"+indice
        for reac in NewModel.reactions:
            reac.id=reac.id+"_"+indice
            if type(reac.name)==type("string"):
                reac.name=reac.name+"_"+indice
            if type(reac.subsystem)==type("string"):
                reac.subsystem=reac.subsystem+"_"+indice
        for metab in NewModel.metabolites:
            metab.id=metab.id+"_"+indice
            if type(metab.name)==type("string"):
                metab.name=metab.name+"_"+indice
            if type(metab.compartment)==type("string"):
                metab.compartment=metab.compartment+"_"+indice
        return NewModel

    def finderOfEX(model):
        '''
            Retrun a dictList of cobra reactions starting with EX
        '''
        res=[]
        for x in model.reactions:
            if type(x.id)==type("string") and x.id.startswith("EX"): #comparaison des types pour sauter les reactions.. 
                                                                    #..sans noms : x.name de type NoneType.
                res.append(x.id)
        return res

    #Importation
    from cobra import Model, Reaction, Metabolite
    
    #Initialisation
    NewModel = cobra.Model("Fusion des modèles !")
    modelList=[]
    
    #Change Name:
    i=0
    for old_model in OldModelList:
        modelList.append(nameChange(old_model,i))
        i+=1
        
    #Ajout de toutes les réactions dans le nouveau modèle : 
    for model in modelList:
        NewModel.add_reactions(model.reactions)
    
    
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
        poolReac.name='Reaction : '+rootMetabtemp.id+'_pool <->'
        poolReac.subsystem = 'pool'
        #Bounds will be set by the diet.
        poolReac.add_metabolites({
            poolMetab : -1.0
        })
        NewModel.add_reactions([poolReac])
    return NewModel

fusion([mini,mini]).reactions
