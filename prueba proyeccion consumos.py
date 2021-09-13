# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 09:15:45 2020

@author: Gabri
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from funciones_AG import pob_ini,bi_to_hex,pob_new

N=7

##Parametros iniciales AG
Npoblacion=50 #El numero de individuos en nuestra poblacion #Multiplo de 2
generaciones=25 #Numero de generaciones
cruce=0.8 #Probabilidad de cruce
mutacion=0.2 #Probabilidad de mutacion
gen=15 #Numero de cromosomas por individuo (Posibles soluciones 2**gen)
variables=3 #Cantidad de variables de nuestra funcion de fitness
alpha=1 #Parametro para acotar las soluciones
bias=0 #Parametro para acotar las soluciones y= alpha*x + b (siendo x el resultado de los genes de un individuo)
FitnessGeneracion=[] ##Guarda el mejor fitness por generacion para llevar control


mainpath="C:/Users/Gabri/Documents/python codes/prueba proyeccion consumos"
filepath="/TEST.xlsx"
data=pd.read_excel(mainpath+filepath)
CODIGO_SIC=data[0].unique().tolist()




#data_consumos=data.transpose()
#p=data_consumos.iloc[3:,0].tolist()
PredT=[]
for frt in CODIGO_SIC:
    p=data[data[0]==frt].iloc[0,3:].tolist()
    T=[]
    for i in range(len(p)):
        T.append(i+1)
        
    df=pd.DataFrame({CODIGO_SIC[0]:p,"T":T})
    lm = smf.ols(formula=CODIGO_SIC[0]+"~T", data=df).fit()
    [X,Y]=lm.params
    pred = lm.predict(pd.DataFrame(df["T"]))
    div=[]
    for x in range(len(pred)):
        div+=list([p[x]/pred[x]])
    ind_i=ind_f=[]
    for x in range(N):
        ind_i=[]
        ind_i+=list([div[x]])
        n=x
        while n+N<len(div):
            n=n+N
            ind_i+=list([div[n]])
        T=[]
        for i in range(len(ind_i)):
            T.append(i+1)
        df=pd.DataFrame({"ind":ind_i,"T":T})
        lm = smf.ols(formula="ind"+"~T", data=df).fit()
        [b1,b2]=lm.params
        ind_f+=list([b1])
    
    int_help=ind_f
    ###Necesito optimizamar a,b,g
    #Algoritmo genetico
    ##Generamos la poblacion incial
    poblacion=pob_ini(variables,Npoblacion,gen)
    for g in range(generaciones):
        ###### Fitness
        ##Pasamos de binario a hexadecimal 
        Fitness=[]
        Rvariables = bi_to_hex(poblacion,variables,alpha,bias)
        ##funcion de fitness###############################    
        for variable in Rvariables: #X va a ser la lista que tenga las nVariables para la funcion
            St=[]
            Bt=[]
            Ct=[]
            St=list([X])
            Bt=list([Y])
            Ct=np.asarray(ind_f)
            dt=[]
            et=[]
            for x in range(len(p)):
                St+= list([ variable[0]*(p[x]/Ct[x]) + (1-variable[0])*(St[x]-Bt[x]) ])
                Bt+= list([ variable[1]*(St[x+1]-St[x]) + (1-variable[1])*Bt[x] ])
                Ct= np.append(Ct, variable[2]*(p[x]/St[x+1]) + (1-variable[2])*Ct[x] )
                dt+= list([ (St[x+1]+Bt[x+1])*Ct[x+N]  ])
                et+=list([ abs(dt[x]-p[x]) ])
            Fitness+=list([1/np.asarray(et).sum()])
        FitnessGeneracion, poblacion=pob_new(Fitness,Rvariables,FitnessGeneracion,variables,poblacion,cruce,mutacion)
          
    FitnessGeneracion=pd.DataFrame(FitnessGeneracion,columns=["Fitness","Variables"])
    resultado=FitnessGeneracion[FitnessGeneracion["Fitness"]==FitnessGeneracion["Fitness"].max()].iloc[0,:].tolist()
    
    ##Mostramos el resultado
    print("Las mejores varibles que se adecuan al problema son:")
    i=1
    for x in resultado[1]: #resultado[1] las variables
        print("Variable[{0}]= {1}".format(i,x))
        i=i+1
    print("Con una fitnes de ",resultado[0]) #resultado[0] la fitness que consiguio
    
    ##Calculamos segun nuestro mejor resultado
    St=list([X])
    Bt=list([Y])
    Ct=np.asarray(ind_f)
    dt=[]
    et=[]
    for x in range(len(p)):
        St+= list([ resultado[1][0]*(p[x]/Ct[x]) + (1-resultado[1][0])*(St[x]-Bt[x]) ])
        Bt+= list([ resultado[1][1]*(St[x+1]-St[x]) + (1-resultado[1][1])*Bt[x] ])
        Ct= np.append(Ct, resultado[1][2]*(p[x]/St[x+1]) + (1-resultado[1][2])*Ct[x] )
        dt+= list([ (St[x+1]+Bt[x+1])*Ct[x+N]  ])
        et+=list([ abs(dt[x]-p[x]) ])
    ##Ahora el vector de prediciones N veces en el futuro
    Pred=[frt]
    for x in range(N):
        if (St[-1]+Bt[-1]*x)*Ct[-1-N+x] > 0:
            Pred+=list([(St[-1]+Bt[-1]*x)*Ct[-1-N+x]])
        else:
            Pred+=list([0])
    PredT.append(Pred)
data_pred=pd.DataFrame(PredT)
data=pd.merge(left= data, right=data_pred,how="outer",left_on=0,right_on=0)
    
    
    
    