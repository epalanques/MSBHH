#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:30:56 2018

@author: grom
"""
from main1 import changerFluxes

def thresholdBiomass(model,diet,threshold):
    '''
    ---args---
    model: a cobra model = the model you want to test
    diet: string = path to a diet.xls
    threshold : float 
    returns TRUE if the model have a biomass>threshold with the given diet, FALSE otherwise.
    '''
    res=False
    changerFluxes(diet,model)
    if model.optimize() > threshold:
        res=True
    return res

'''HOW TO KNOW THE VALUE OF THE THRESHOLD ?'''