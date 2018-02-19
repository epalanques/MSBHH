import compara
import os
from os import listdir
from os.path import isfile, join
import pandas
from collections import Counter

def main(diets, models, dict, equi):
    #diets and models are lists
    mat = []
    p = {}
    lmt = []
    ldt = []
    for diet in diets:
        ligneMat = []
        for model in models:
            d = {}
            ld = []
            ld = []
            d, ld, lm = compara.comparer(diet, model, d)
            bm = compara.modifier(d, model)
            print("dades:")
            print(diet.split("/")[-1])
            print(model.split("/")[-1])
            print(bm)
            print("----")
            ligneMat.append(bm)
            #on cree un dictionnaire global
            for key in d:
                if key not in p:
                    p[key]=d[key]
                    if equi:
                        lmt = lmt + lm
                        ldt = ldt+ ld
        mat.append(ligneMat)
    x = pandas.DataFrame(mat)
    print("uuu")
    print(x)
    if dict:
        compara.dictionaire_xls(p)
    if equi:
        compara.differences_xls(p,ldt, lmt)
    #on Reecris les noms pour qu'il soit jolies
    dietsmod = []
    modelsmod = []
    for diet in diets:
        diet = diet.split("/")
        diet = diet[-1].split(".")
        dietsmod.append(diet[0])
    for model in models:
        model = model.split("/")
        model = model[-1].split(".")
        modelsmod.append(model[0])
    print("----")
    print("Models:")
    print(modelsmod)
    print("----")
    print("dietes:")
    print(dietsmod)
    x = pandas.DataFrame(mat,dietsmod, modelsmod)
    print(x)
    nd = {}
    return x

    
