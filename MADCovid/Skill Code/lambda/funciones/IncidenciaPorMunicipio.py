import requests
import json
import datetime
from ask_sdk_core.utils import get_slot_value

def handle (handler_input):
    municipio = get_slot_value(handler_input=handler_input, slot_name="municipio")
    
    varios_municipios = handler_input.request_envelope.request.intent.slots["municipio"].resolutions.resolutions_per_authority[0].values
    tamanyo = len (varios_municipios)
    if tamanyo > 1: # el usuario está preguntando por un municipio en el que hay varios que se llaman parecido. Ej: pregunta por torrejón y hay tres torrejones, torrejón de Ardoz, Torrejón de Velasco y Torrejón de la Calzada
        speak_output = " A qué "+municipio+" te refieres: "
        for i in range (0,tamanyo):
            speak_output += " "+varios_municipios[i].value.name+", "
        handler_input.attributes_manager.session_attributes["set_incidencia_municipio"] = True
    elif tamanyo == 1: 
        municipio = varios_municipios[0].value.name
        
        datos_covid = requests.get ("https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/877fa8f5-cd6c-4e44-9df5-0fb60944a841/download/covid19_tia_muni_y_distritos_s.json")
        
        if datos_covid.status_code == 200:
            datos = json.loads (datos_covid.content)
            
            if len(datos) == 0:
                speak_output = "No se han encontrado datos para ese municipio."
            else: 
                datos = datos["data"]
                for i in range (199):
                    if 'municipio_distrito' in datos[i] and 'casos_confirmados_ultimos_14dias' in datos[i] and datos[i]["municipio_distrito"] == municipio:
                        speak_output = "En "+municipio+" hay una incidencia de "+str(datos[i]['casos_confirmados_ultimos_14dias'])+" casos por cada cien mil habitantes"
        else: 
            speak_output = "Vaya!, algo ha ido mal. Inténtalo de nuevo más tarde."

    elif tamanyo == 0:
        speak_output = "No existe ningún municipio con el nombre que indicas."



    return speak_output