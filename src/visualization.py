
import sys
sys.path.append("../")
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys
import re
import src.visualization as vs
sns.set_context("poster")
sns.set(rc={"figure.figsize": (12.,6.)})
sns.set_style("whitegrid")

import plotly.express as px
import plotly.graph_objects as go



def health(df):
    """
    La columna healthLabels de mi dataframe contiene una lista con mucha información de cada alimento,
    para conseguir esta, he creado esta función que le pide al usuario un ingrediente que debe estar incluido
    en la lista de alimentos/ingredientes del dataframe, para que me devuelva toda la información
    contenida de dicho alimento"""

    valor1=input("Ingrese un ingrediente:")

    res = df[df["Food"] == valor1]
    return list(res["healthLabels"])



def comparative(df):

    """
    Con esta función consigo que al ingresar el usuario dos ingredientes, me devuelva una gráfica
    comparando de ambos ingredientes/alimentos los valores de Calcio y Vitamina C de cada uno"""
    valor_1=input("Ingrese un ingrediente:")
    valor_2=input("Ingrese un ingrediente:")

    res1 = df[(df["Food"] == valor_1 )| (df["Food"] == valor_2)]
 
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,10),sharey = True) 
    sns.barplot(y="Calcium(mg)", x = "Food", data = res1,  palette="mako", ax=ax[0])
    sns.barplot(y="VIT C(mg)", x = "Food", data = res1,  palette="mako", ax=ax[1]);