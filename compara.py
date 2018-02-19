import cobra
import cobra.test
import os
from os.path import join
import pandas
import difflib
import xlsxwriter

def comparer(diet = "", model= "", d = {}, ldiet_out = [], lmod_out = []):
    #a canviar diet i model
    ldiet_in = []
    lmod_in = []
    df = pandas.read_excel(diet)
    ids = df['reaction'].values
    fluxes = df['fluxValue'].values
    values = []
    print("En Compara:")
    print(model)
    print(diet)
    print(len(d))
    for i in range(len(fluxes)-1):
        values.append((ids[i],fluxes[i]))
    model = cobra.io.read_sbml_model(model)
    for val in values:
        v = val[0]
        f = val[1]
        l1 = v.split("_")
        ns1 = "".join(l1) #il efface les _
        if ns1.startswith("EX"): #ns1: reactions de la diete qui commençont par "EX"
            for rec in model.reactions:
                if rec.id.startswith("EX"):
                    l = rec.id.split("_")
                    l2 = treupar(l)#il change LPAREN par ( et RPAREN par ) 
                    ns = "".join(l2) #il efface les _
                    if ns.startswith(ns1):
                        d[v] = [rec.id, rec.reaction, rec.name, f]
                        lmod_in.append(rec.id)
                        ldiet_in.append(v)
                        for val in values:
                            if val[0] not in ldiet_in:
                                ldiet_out.append(val)
    for rec in model.reactions: #totes les reaccions
        if rec.id.startswith("EX"): #reaccions del model que comencen amb EX
            if rec.id not in lmod_in:
                lmod_out.append((rec.id, rec.reaction,rec.name))
    print(model.optimize().f)
    return (d,ldiet_out,lmod_out)

def modifier(d, model):
    model = cobra.io.read_sbml_model(model)
    for key in d:
        try:
            pgi = model.reactions.get_by_id(d[key][0])
            bound =d[key][3]
            #print(pgi.lower_bound)
            #print(pgi.upper_bound)
            pgi.lower_bound = - bound
            pgi.upper_bound = 0
            #print(pgi.lower_bound)
            #print(pgi.upper_bound)
        except KeyError:
            pass
    print(len(d))
    print("fi main")
    return model.optimize().f
        
    
def treupar(ll):
    for i in range(len(ll)):
        if ll[i] == "LPAREN":
            ll[i] = "("
        if ll[i] == "RPAREN":
            ll[i] = ")"
    return ll
    
#def bounds(d):
#    df = pandas.read_excel("fluxes.xls")
 #   values = df['fluxValue'].values
  #  model = cobra.io.read_sbml_model("pyogenes.xml")
   # model.optimize()
    #return model
              
    
def differences_xls(d, ldiet,lmodel):
    workbook = xlsxwriter.Workbook("differences.xlsx")
    worksheet = workbook.add_worksheet()
    model = cobra.io.read_sbml_model("pyogenes.xml")
    worksheet.write(0,0,"DIETE")
    worksheet.write(0,2,"MODELE_ID")
    worksheet.write(0,3,"MODELE_NAME")
    worksheet.write(0,4,"MODELE_REACTIONS")
    row = 1
    for die in ldiet:
        if die in d:
            print("erreur")
        print("aqui:")
        print(die)
        worksheet.write(row,0, die[0])
        row = row+1
    row = 1
    for m in lmodel:
        for k in d:
            if m in d[k]:
                print("erreur")
                print(m[0])
        worksheet.write(row,2, m[0])
        worksheet.write(row,3, m[1])
        worksheet.write(row,4, m[2])
        row = row+1
    workbook.close()

def dictionaire_xls(d):
    workbook = xlsxwriter.Workbook("dictionaire.xlsx")
    worksheet = workbook.add_worksheet()
    model = cobra.io.read_sbml_model("pyogenes.xml")
    worksheet.write(0,0,"DIETE")
    worksheet.write(0,1,"MODELE_ID")
    worksheet.write(0,2,"REACTION")
    worksheet.write(0,3,"MODELE_NOM")
    worksheet.write(0,4,"FLUX")
    row = 1
    for k in d:
        print(k)
        worksheet.write(row,0,k)
        worksheet.write(row,1,d[k][0])
        worksheet.write(row,2,d[k][1])
        worksheet.write(row,3,d[k][2])
        worksheet.write(row,4,d[k][3])
        row = row+1
    workbook.close()

def maxflux(m):
    l = []
    mf = []
    for rec in m:
        l.append(rec.flux)
    for i in range(len(l)):
        if i<5:
            mf.append(l[i])
        else:
            if l[i]>min(mf):
                mf.pop
