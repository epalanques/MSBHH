import cobra
import cobra.test
import os
from os.path import join
import pandas
import difflib
import xlsxwriter


#  model = cobra.io.read_sbml_model("pyogenes.xml")

def echangesDiete(diete, d={}, ldiet_out=[], lmod_out=[]):
    # *****************  posar a part el calculador de la dieta i del model.
    # imports
    df = pandas.read_excel(diete)  # Importation de la diete

    # inicialisacion des variables
    ids = df['reaction'].values
    fluxes = df['fluxValue'].values

    ldiet_in = []
    lmod_in = []

    echangesDiete = []

    # obtention de la liste des reactions d'echange de la diete
    for i in range(len(fluxes) - 1):
        reacIdDiet = ids[i]
        flux = fluxes[i]

        if reacIdDiet.startswith("EX"):
            # On ajoute l'identifiant propre à la liste
            idPropreDiete = traitement(reacIdDiet)
            echangesDiete.append((idPropreDiete, reacIdDiet, flux))

    return echangesDiete


def echangesModele(modele, critere="pool", d={}, ldiet_out=[], lmod_out=[]):
    echangesModele = []
    # obtention de la liste des reactions d'echange du modele
    for rec in modele.reactions:

        # Obtention des reactions d'echange
        if rec.id.startswith(critere):
            # Ona ajoute l'identifiant propre à la liste
            idPropreModele = traitement(rec.id)
            echangesModele.append((rec, idPropreModele))

    return echangesModele


def comparerEchanges(echangesModele, echangesDiet, lenPref=4):
    # Inicialisation des variables
    correspondances = {}
    nonCorrespondantsDiete = []
    nonCorrespondantsModele = []
    reactionsModelAjoutees = []

    # Comparation d'identifiants
    for reacEchangeDiet in echangesDiet:
        idPropreDiet = reacEchangeDiet[0]
        idDiet = reacEchangeDiet[1]
        flux = reacEchangeDiet[2]

        correspondance_trouve = False

        for reacEchangeModele in echangesModele:
            idPropreModel = reacEchangeModele[1]
            reaction = reacEchangeModele[0]

            if idPropreDiet[2:].startswith(idPropreModel[lenPref:]):
                # Correspondence entre identifiants
                # Creation du dictionnaire

                correspondances[idDiet] = [reaction, flux]

                correspondance_trouve = True
                reactionsModelAjoutees.append(reaction)

        if not correspondance_trouve:
            # on ajoute reactions de la diete qui n'ont pas trouve un correspondant
            nonCorrespondantsDiete.append((idPropreDiet, idDiet))

    for reacEchangeModele in echangesModele:
        if reacEchangeModele[1] not in reactionsModelAjoutees:
            # on ajoute les reactions du modele qui n'ont pas trouve un correspondant
            nonCorrespondantsModele.append(reaction)

    return (correspondances, nonCorrespondantsModele, nonCorrespondantsDiete)


def modifierFluxes(correspondances):
    for reactionID in correspondances:
        reaction = correspondances[reactionID][0]
        flux = correspondances[reactionID][1]
        reaction.lower_bound = - flux
        reaction.upperbound = 0

    return


def traitement(mot):
    # fonction pour traiter les mots
    # On peut ajouter plus de modifications pour identifiants plus diferents

    # On supprime les "_" et les "(" ")"
    elem = mot.split("_")

    for i in range(len(elem)):
        if elem[i] == "LPAREN":
            elem[i] = "("
        if elem[i] == "RPAREN":
            elem[i] = ")"

    mot = "".join(elem)

    return mot


# def bounds(d):
#    df = pandas.read_excel("fluxes.xls")
#   values = df['fluxValue'].values
#  model = cobra.io.read_sbml_model("pyogenes.xml")
# model.optimize()
# return model


def nonCorrespondants_xls(nonCorrespondantsDiete, nonCorrespondantsModele):
    # creacion de l'excel
    workbook = xlsxwriter.Workbook("differences.xlsx")
    worksheet = workbook.add_worksheet()

    # on ajoute les titres de colonnes
    worksheet.write(0, 0, "DIETE")
    worksheet.write(0, 2, "MODELE_ID")
    worksheet.write(0, 3, "MODELE_NAME")
    worksheet.write(0, 4, "MODELE_REACTION")

    # On ajoute les nonCorrespondants de la diete
    row = 1
    for reaction in nonCorrespondantsDiete:
        worksheet.write(row, 0, reaction[1])
        row = row + 1

    # On ajoute les nonCorrespondants du modele
    row = 1
    for reaction in nonCorrespondantsModele:
        worksheet.write(row, 2, reaction.id)
        worksheet.write(row, 3, reaction.name)
        worksheet.write(row, 4, reaction.reaction)
        row = row + 1

    # fermeture de l'xls
    workbook.close()


def correspondants_xls(correspondants):
    # ouverture de l'xls
    workbook = xlsxwriter.Workbook("dictionaire.xlsx")
    worksheet = workbook.add_worksheet()

    # on met les titres des colonnes
    worksheet.write(0, 0, "DIETE_ID")
    worksheet.write(0, 1, "MODELE_ID")
    worksheet.write(0, 2, "MODELE_NAME")
    worksheet.write(0, 3, "MODELE_REACTION")
    worksheet.write(0, 4, "FLUX")

    # on ajoute les valeurs du dictionaire
    row = 1
    for reaction in correspondants:
        worksheet.write(row, 0, reaction)  # dieteID
        worksheet.write(row, 1, correspondants[reaction][0].id)  # modeleID
        worksheet.write(row, 2, correspondants[reaction][0].name)  # modeleName
        worksheet.write(row, 3, correspondants[reaction][0].reaction)  # modeleReaction
        worksheet.write(row, 4, correspondants[reaction][1])  # flux
        row = row + 1

    # fermeture de l'excel
    workbook.close()


