import compara
import pandas
import cobra

def changerFluxes(diete, modele):

    #On extrait les donnees pour modifier les fluxes
    echDie = compara.echangesDiete(diete)
    echMod = compara.echangesModele(modele, "EX")
    corr, nonCorDie, nonCorMod = compara.comparerEchanges(echMod, echDie,2)

    #On change les fluxes
    compara.modifierFluxes(corr)

    return modele



def main1(dietes, models):

    biomasses = []
    for diete in dietes:
        matrixLigne = []
        for modele in models:
            mod = cobra.io.read_sbml_model(modele) #On lit le modele
            m = changerFluxes(diete, mod) #On change son flux
            bm = m.optimize().f #On en obtient la biomasse
            matrixLigne.append(bm) #On ajoute la biomasse resultant dans une ligne de la matrice

        biomasses.append(matrixLigne) #On ajoute la ligne de la matrice dans la matrice

    #Conversion de la matrice en dataFrame de pandas
    ## Obtention des noms
    nomModels = netoyeNoms(dietes)
    nomDietes = netoyeNoms(models)
    print(nomModels)
    print (nomDietes)
    biomasses = pandas.DataFrame(biomasses, nomModels, nomDietes)

    return biomasses

def netoyeNoms(fixiers):
    fNetoyes = []
    for fixier in fixiers:
        netoye = fixier.split("/")
        netoye = netoye[-1][:-4]
        fNetoyes.append(netoye)
    return fNetoyes


def listeDietes():
    diets = []
    for i in range(10):
        s = "d" + str(i+1) + ".xls"
        diets.append(s)
    return diets