from datetime import datetime
import json
import os

def validar_dia(dia):

    dias_validos = [
        "Lunes",
        "Martes",
        "Miercoles",
        "Jueves",
        "Viernes",
    ]
    return dia in dias_validos

def valida_hora(hora):
    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False

def convertir_minutos(hora):

    horas, minutos = map(int, hora.split(":"))

    return horas * 60 + minutos


def rango_hora(hora_inicio, hora_final):

    return convertir_minutos(hora_inicio) < convertir_minutos(hora_final)

ARCHIVO = "horario.json"
def cargar_horario():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return []

def guardar_horario(horario):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(horario, archivo, indent=4, ensure_ascii=False)

def valida_conflicto(horario_semanal, horario_temporal):

    inicio_temporal= convertir_minutos(horario_temporal["hora_inicio"])
    fin_temporal= convertir_minutos(horario_temporal["hora_fin"])

    for actividad in horario_semanal:

        if actividad["dia"]==horario_temporal["dia"]:

            inicio_actividad= convertir_minutos(actividad["hora_inicio"])
            fin_actividad= convertir_minutos(actividad["hora_fin"])

            if (inicio_temporal < fin_actividad and fin_temporal > inicio_actividad):
                return True

    return False