import re
import requests 
import json
import os
from dotenv import load_dotenv
import pandas as pd
from pandas import json_normalize





def call_api(app_id, app_key, lista_food):

    """ con esta función hago la llamada a la API que he utilizado para enriquecer mi dataframe, 
    esta me pide tres atributos, 2 tokens e incluir un ingrediente, en este caso he incluido 
    la lista de ingredientes o alimentos de mi data frame inicial
    """
    result_list = []
    for ingre in lista_food: 
        b = requests.get(f'https://api.edamam.com/api/nutrition-data?app_id={app_id}&app_key={app_key}&nutrition-type=logging&ingr={ingre}').content
        r = json.loads(b.decode())#esta API concretamente me devuelve el string de un diccionario, uso decode para que me devuelva solo en diccionario
        result_list.append(r)
    return result_list