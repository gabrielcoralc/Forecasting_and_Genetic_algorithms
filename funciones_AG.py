# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:18:00 2020

@author: Gabri
"""
##Cuando realice este algoritmo, fue debido a que no encontre una libreria que realizar un proceso de optimizacion
# de las variables de una funcion, o al menos no encontre alguna que pudiera entender, por lo que realice
#estan funciones basadas en los algortimos de optimizacion en algoritmos geneticos, en donde
#una poblacion inicial de valores se va modificando de manera que se acerque al mejor posible segun
#una funcion de fitness.
#Este codigo lo realice cuando apenas estaba aprendiendo programacion en python, por lo que deberia tener mucho por mejorar
#tanto en simplicidad del codigo, como que se deberia crear un empaquetado de todas las funciones.


import numpy as np
import pandas as pd

def pob_ini(variables,Npoblacion,gen):
    """La funcion crea las matrices con valores binarios que se considera como la poblacion inicial para un algoritmo genetico
        Parameters
        ----------
        variables : int
            Numero de variables que queremos trabajar
        Npoblacion : int
            El numero de individuos en nuestra poblacion. Esta debe ser un Multiplo de 2
        Gen: int
            El numero de genes que va a tener cada individuo
        Returns
        -------
        list(list(np.array))
            Retorna una lista de lista, en cada lista hay una matriz con valores binarios que representa la poblacion de cada variable
        """
    
    poblacion={}
    for x in range(variables): ##Se genera un poblacion de Npoblacion individuos para cada Variable
        p=[]
        for xx in range(Npoblacion):
            A=np.random.randint(2,size=gen)
            p+=list([A])
        poblacion[x]=p
    return poblacion

def bi_to_hex(poblacion,variables,alpha,bias):
    """La funcion hace la transformacion de los individuos, el cual es un vector que representa un numero binario pasarlo a hexadecimal
        y asi usalor en nuestra funcion de fitness
    Parameters
    ----------
    poblacion : list(list(np.array))
        Lista de matrices que represanta la poblacion en algortimos geneticos
    variables : int
        Numero de variables que queremos trabajar
    alpha: int
        Valor que acota las posibles soluciones de cada individuo entre (0,alpha)
    bias: int
        Parametro para acotar las soluciones y= alpha*x + b (siendo x el resultado de los genes de un individuo)
    Returns
    -------
    list(list(np.array))
        Retorna una nueva poblacion
    """
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
    
    """La funcion modifica la poblacion que se le entrega, apartir de un proceso en donde se eligen las mejores 
        soluciones apartir de su fitness, y estas son modificadas en un proceso de cruce y de mutacion
    Parameters
    ----------
    Fitness : list(list())
        Lista de matrices que represanta la poblacion en algortimos geneticos
    Rvariables : list(np.array)
        Es el resultado de utilizar la funcion bi_to_hex()
    FitnessGeneracion: list
        una lista de los fitness que tiene cada generacion para llevar el control
    variables: int
        umero de variables que queremos trabajar
    poblacion : list(list(np.array))
        Lista de matrices que represanta la poblacion en algortimos geneticos
    cruce : float
        Probabilidad entre (0,1) de que un individuo realice el proceso de cruce
    mutacion : float
        Probabilidad entre (0,1) de que un individuo realice el proceso de mutacion    
    Returns
    -------
    poblacion: list(np.array)
        Retorna la poblacion modificada
    FitnessGeneracion: list()
        Retorna un lista con la mejor fitness por Generacion
    """
    
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