import requests
import json
import datetime
from ask_sdk_core.utils import get_slot_value

def handle (handler_input):

    datos_covid = requests.get ("https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/877fa8f5-cd6c-4e44-9df5-0fb60944a841/download/covid19_tia_muni_y_distritos_s.json")
    
    if datos_covid.status_code == 200:
        datos = json.loads (datos_covid.content)
            
        if len(datos) == 0:
            speak_output = "No se han encontrado datos para ese municipio."
        else: 
            datos = datos["data"]
            casos_totales = 0
            tamanyo = len(datos)
            for i in range (199):
                if 'casos_confirmados_totales' in datos[i]:
                    casos_totales = casos_totales + int (datos[i]['casos_confirmados_totales'])
                else:
                    casos_totales = casos_totales + 0
            speak_output = "En la Comunidad de Madrid se han confirmado un total de "+str(casos_totales)+" casos desde el 25 de febrero de 2020."
    else: 
        speak_output = "Vaya!, algo ha ido mal. Inténtalo de nuevo más tarde."

    return speak_output