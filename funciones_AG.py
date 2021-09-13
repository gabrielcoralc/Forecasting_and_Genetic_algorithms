# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:18:00 2020

@author: Gabri
"""

def pob_ini(variables,Npoblacion,gen):
    import numpy as np
    poblacion={}
    for x in range(variables): ##Se genera un poblacion de Npoblacion individuos para cada Variable
        p=[]
        for xx in range(Npoblacion):
            A=np.random.randint(2,size=gen)
            p+=list([A])
        poblacion[x]=p
    return poblacion

def bi_to_hex(poblacion,variables,alpha,bias):
    Rvariables=[]
    for x in range(len(poblacion[0])):
        var=[]
        for xx in range(variables):
            bandera1=poblacion[xx][x]
            bandera2=0
            for xxx in range(bandera1.shape[0]-1):
                if bandera1[xxx]==1:
                    bandera2=bandera2+2**(bandera1.shape[0]-1-xxx)
            ##En este caso necesitamos valores entre 0 y aplha
            bandera2=((bandera2*alpha)/2**(bandera1.shape[0]-1))+bias
            var+=list([bandera2])
        Rvariables+=list([var])#Variables a ingresar en la funcion a evaluar
    return Rvariables

def pob_new(Fitness,Rvariables,FitnessGeneracion,variables,poblacion,cruce,mutacion):
    import pandas as pd
    import numpy as np
    
    df=pd.DataFrame({"Fitness":Fitness,"Coef":Rvariables})
    SortedFitness=sorted(Fitness)
    MattingP=[]
    for x in range(len(SortedFitness)):
        MattingP+=list([SortedFitness[x]/df["Fitness"].values.sum()])
    FitnessGeneracion.append([df[df["Fitness"]==df["Fitness"].max()].iloc[0,0], df[df["Fitness"]==df["Fitness"].max()].iloc[0,1]])
    
    ##Cruce
    Nuevapoblacion={}
    for y in range(variables):
        hijos=[]
        for x in range(int(len(poblacion[0])/2)):
            Padres={}
            for z in range(2):
                ##Selecionamos los padres
                NumeroA=np.random.rand()
                i=0
                xx=0
                while i==0:
                    if len(MattingP)-1-xx==0:
                        i=1
                    else:
                        if MattingP[len(MattingP)-1-xx]<NumeroA:
                            i=1
                        else:
                            xx=xx+1
                Padres[z]=poblacion[y][df[df["Fitness"]==SortedFitness[len(MattingP)-1-xx]].index[0]]
            ## Hay cruce o no 
            NumeroA=np.random.rand()
            if NumeroA<cruce:
                NumeroA=np.random.randint(len(Padres[0])-1)
                hijos+=list([np.append(Padres[0][0:NumeroA],Padres[1][NumeroA:])])
                hijos+=list([np.append(Padres[1][0:NumeroA],Padres[0][NumeroA:])])
            else:
                hijos+=list([Padres[0]])
                hijos+=list([Padres[1]])
            ##Mutacion?
            for z in range(2):
                for w in range(len(hijos[0])):
                    NumeroA=np.random.rand()
                    if NumeroA<mutacion:
                        if hijos[x+z][w] == 1:
                            hijos[x+z][w] = 0
                        else:
                            hijos[x+z][w] = 1
        Nuevapoblacion[y]=hijos
    poblacion=Nuevapoblacion ##Tenemos nueva generacion
    return FitnessGeneracion, poblacion