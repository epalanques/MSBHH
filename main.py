import compara


def changerFluxes(diete, modele):

    #On extrait les donnees pour modifier les fluxes
    echMod, echDie = compara.trouverEchanges(diete, modele)
    corr, nonCorDie, nonCorMod = compara.comparerEchanges(echMod, echDie)

    #On change les fluxes
    compara.modifierFluxes(corr)

    return modele


    
