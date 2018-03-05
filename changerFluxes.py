import compara


def changerFluxes(diete, modele):

    #On extrait les donnees pour modifier les fluxes
    echDie = compara.echangesDiete(diete)
    echMod = compara.echangesModele(modele)
    corr, nonCorDie, nonCorMod = compara.comparerEchanges(echMod, echDie)

    #On change les fluxes
    compara.modifierFluxes(corr)

    return modele


    
