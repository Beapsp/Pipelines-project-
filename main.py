import json
import os
from dotenv import load_dotenv
import pandas as pd
from pandas import json_normalize
import sys
sys.path.append('../')
import src.cleaning_functions as cf

load_dotenv()

pd.set_option('display.max_columns', None) #con este parámetro puedo ver TODAS las columnas de un df.
df= pd.read_csv("data/Food and Calories.csv")

#Tras la importación de las librerias, csv y métodos necesarios comienzo con la limpieza del dataframe importado.

#1. Elimino nulos y duplicados
df.dropna(how="all", inplace=True)
duplicates= df.drop_duplicates() #elimino los duplicados

food = duplicates["Food"].unique()
#2. Obtengo la lista de alimentos que voy a usar para todo el proceso de enriquecimiento de df y comprobación de hipótesis.
lista_food= list(food)

#3. Apilico la función definida, la cual me hará la llamada a la API escogida para enriquecer mi dataframe. Esta requiere 3 parámetros.
api_id = os.getenv("app_id")
app_key = os.getenv("app_key")

prueba2 = cf.call_api(api_id,app_key,lista_food)

#4. Convierto la información obtenida de la API en un dataframe
df_api = json_normalize(prueba2)

#5. Como cuento con un dataframe a partir de mi API con muchas columnas cuya información no es relevante para mi proyecto, creo un df nuevo con las columnas requeridas.
df_clean = df_api[["dietLabels","healthLabels","cautions","totalNutrients.FAT.quantity","totalNutrients.SUGAR.quantity","totalNutrients.PROCNT.quantity","totalNutrients.CHOLE.quantity","totalNutrients.CA.quantity","totalNutrients.VITC.quantity","totalNutrients.WATER.quantity","totalNutrients.SUGAR.added.quantity"]]
df_clean["Ingredient"] = lista_food
# Incluyo una columna nueva al df de la API limpio, la cual está compuesta de los alimentos de la lista creada a partir del dataframe inicial


# Renombro las columnas de mi dataframe limpio
rename = {"totalNutrients.FAT.quantity": "FAT.Total lipid","totalNutrients.SUGAR.quantity":"Total SUGAR(g)","totalNutrients.PROCNT.quantity":"Total PROTEIN(g)","totalNutrients.CHOLE.quantity":"Cholesterol(mg)","totalNutrients.CA.quantity":"Calcium(mg)","totalNutrients.VITC.quantity":"VIT C(mg)","totalNutrients.WATER.quantity":"Whater quantity","totalNutrients.SUGAR.added.quantity":"Sugar added"}
df_clean.rename(columns=rename, inplace=True)

#6. Ahora cuento con dos dataframe que comparten una columna común, por lo que puedo unirlos a través de esta, quedándome después únicamente con una. 
mergeado = df_clean.merge(duplicates, how="left", left_on = "Ingredient", right_on="Food")
mergeado.drop(columns=["Ingredient"], inplace=True)
#Reordeno las columnas para un mejor entendimiento del dataframe
mergeado = mergeado.reindex(columns=['Food','Serving','Calories','dietLabels','healthLabels','cautions','FAT.Total lipid','Total SUGAR(g)','Total PROTEIN(g)','Cholesterol(mg)','Calcium(mg)','VIT C(mg)','Whater quantity','Sugar added'])

print(mergeado)
#7. Importo mi nuevo csv
mergeado.to_csv("data/Food_enriched.csv")
