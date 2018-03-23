#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:38:31 2018

@author: grom
"""
import thresholdBiomass.py
from minSharedReactions import *
from cobra import *

def Caracterisation(model1,model2,threshold):
    '''
        model1,2 : 2 cobra models
        threshold: integer = number min of shared reactions
    '''
    if compareReactions(model1,model,threshold):
        
        
    else:
        print("Number of reactions lower than the fixed threshold")
        