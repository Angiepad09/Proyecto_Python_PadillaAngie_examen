from validacion import *
import json

def registrar_actividad(horario_semanal):
    
    horario_semanal = cargar_horario()
    while True:
        materia=input("Ingrese el nombre de la materia o actividad->").strip().capitalize()
        
        if materia !="":
            break
        print("El nombre de la materia o actividad no puede estar vacio. Intente de Nuevo\n")
    
    while True:
        dia = input("Ingrese el dia de la semana (Lunes, Martes, Miercoles, Jueves, Viernes)->").strip().capitalize()
        
        if validar_dia(dia):
            break
        print("El dia ingresado no es valido. Intente de Nuevo\n")
        
    while True:
        hora_inicio = input("Ingrese la hora de inicio (HH:MM)-> ").strip()

        if valida_hora(hora_inicio):
            break
        print("La hora de inicio no es válida.\n")

    while True:
        hora_fin = input("Ingrese la hora de fin (HH:MM)-> ").strip()

        if not valida_hora(hora_fin):
            print("La hora de fin no es válida.\n")
            continue

        if not rango_hora(hora_inicio, hora_fin):
            print("La hora de fin debe ser mayor que la hora de inicio.\n")
            continue
        break
    
    ubicacion = input("Ingrese la ubicacion (opcional, ejemplo Salon 305)->").strip().capitalize()

    horario_temporal ={
        "materia": materia,
        "dia": dia,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "ubicacion": ubicacion
    }

    if valida_conflicto(horario_semanal, horario_temporal):
        print("El horario ingresado entra en conflicto con otra actividad registrada. Intente de Nuevo\n")
        return
    
    horario_semanal.append(horario_temporal)
    guardar_horario(horario_semanal)
    
    print(f"La materia '{materia}' ha sido registrada exitosamente el {dia} de {hora_inicio} a {hora_fin} en {ubicacion}\n")

def mostrar_horario():

    horario = cargar_horario()

    if not horario:
        print("No hay actividades registradas.\n")
        return

    dias = ["Lunes","Martes","Miercoles","Jueves","Viernes"]
    
    horas = sorted({actividad["hora_inicio"] for actividad in horario},key=convertir_minutos)

    print("=" * 95)

    print(
        f"{'Hora':<15}"
        f"| {'Lunes':<15}"
        f"| {'Martes':<15}"
        f"| {'Miércoles':<15}"
        f"| {'Jueves':<15}"
        f"| {'Viernes':<15}"
    )

    print("=" * 95)

    for hora in horas:

        print(f"{hora:<15}", end="")

        for dia in dias:
            materia = "Libre"

            for actividad in horario:
                if (actividad["hora_inicio"] == hora and actividad["dia"] == dia):
                    materia = actividad["materia"]
                    break
            print(f"| {materia:<15}", end="")

        print()
        
def modificar_actividad():

    horario = cargar_horario()

    if not horario:
        print("No hay actividades registradas.\n")
        return False

    materia_buscar = input("Ingrese el nombre de la materia o actividad a modificar-> ").strip().capitalize()

    coincidencias = []

    for i, actividad in enumerate(horario):
        if actividad["materia"] == materia_buscar:
            coincidencias.append((i, actividad))

    if len(coincidencias) == 0:
        print(f'No se pudo modificar la materia "{materia_buscar}" porque no existe.\n')
        return False

    if len(coincidencias) == 1:
        indice, actividad_encontrada = coincidencias[0]

    else:

        print(f'\nSe encontraron varias actividades con el nombre "{materia_buscar}":\n')

        for _, actividad in coincidencias:
            print(
                f'- {actividad["dia"]} '
                f'({actividad["hora_inicio"]} - {actividad["hora_fin"]})'
            )

        while True:
            dia_buscar = input("\nIngrese el día de la actividad que desea modificar-> ").strip().capitalize()

            actividad_encontrada = None
            indice = None

            for i, actividad in coincidencias:
                if actividad["dia"] == dia_buscar:
                    indice = i
                    actividad_encontrada = actividad
                    break

            if actividad_encontrada is not None:
                break

            print(f'No existe una materia "{materia_buscar}" el día {dia_buscar}. Intente nuevamente.\n')

    while True:
        nuevo_dia = input("Ingrese el nuevo día de la semana-> ").strip().capitalize()

        if validar_dia(nuevo_dia):
            break

        print("El día ingresado no es válido. Intente de nuevo.\n")

    while True:
        nueva_hora_inicio = input("Ingrese la nueva hora de inicio-> ").strip()

        if valida_hora(nueva_hora_inicio):
            break

        print("La hora de inicio ingresada no es válida. Intente de nuevo.\n")

    while True:
        nueva_hora_fin = input("Ingrese la nueva hora de fin-> ").strip()

        if not valida_hora(nueva_hora_fin):
            print("La hora de fin ingresada no es válida. Intente de nuevo.\n")
            continue

        if not rango_hora(nueva_hora_inicio, nueva_hora_fin):
            print("La hora de fin debe ser mayor que la hora de inicio. Intente de nuevo.\n")
            continue
        break

    nueva_ubicacion = input(f'Ingrese la nueva ubicación (ENTER para mantener "{actividad_encontrada["ubicacion"]}")-> ').strip().capitalize()

    if nueva_ubicacion == "":
        nueva_ubicacion = actividad_encontrada["ubicacion"]

    horario_temporal = {
        "materia": actividad_encontrada["materia"],
        "dia": nuevo_dia,
        "hora_inicio": nueva_hora_inicio,
        "hora_fin": nueva_hora_fin,
        "ubicacion": nueva_ubicacion
    }

    horario_sin_actual = horario.copy()
    horario_sin_actual.pop(indice)

    if valida_conflicto(horario_sin_actual, horario_temporal):
        print(f'No se pudo modificar la materia "{materia_buscar}" porque el nuevo horario entra en conflicto con otra actividad.\n')
        return False

    horario[indice] = horario_temporal

    guardar_horario(horario)

    print(f'Materia "{materia_buscar}" modificada exitosamente a {nuevo_dia} de {nueva_hora_inicio} a {nueva_hora_fin} en {nueva_ubicacion}.\n')

    return True

def eliminar_actividad():

    horario = cargar_horario()

    if not horario:
        print("No hay actividades registradas.\n")
        return False

    materia = input("Ingrese el nombre de la materia o actividad que desea eliminar-> ").strip().capitalize()
    existe = False

    for actividad in horario:
        if actividad["materia"] == materia:
            existe = True
            break

    if not existe:
        print(f'No se pudo eliminar la materia "{materia}" porque no existe.\n')
        return False

    while True:
        dia = input("Ingrese el día de la semana-> ").strip().capitalize()

        if validar_dia(dia):
            break

        print("El día ingresado no es válido. Intente de nuevo.\n")

    for actividad in horario:

        if (actividad["materia"] == materia and actividad["dia"] == dia):

            horario.remove(actividad)
            guardar_horario(horario)
            print(f'La materia "{materia}" ha sido eliminada del horario del día {dia}.\n')
            return True

    print(f'La materia "{materia}" existe, pero no está registrada para el día {dia}.\n')
    return False

def generar_reporte():
    horario = cargar_horario()

    if not horario:
        print("No hay actividades registradas.\n")
        return False

    dias = ["Lunes","Martes","Miercoles","Jueves","Viernes"]

    reporte = []

    print("\n" + "=" * 50)
    print("REPORTE DEL HORARIO SEMANAL".center(50))
    print("=" * 50)

    lineas_mostradas = 0
    limite_lineas = 5

    for dia in dias:

        eventos = []

        actividades_dia = [
            actividad
            for actividad in horario
            if actividad["dia"] == dia
        ]

        actividades_dia.sort(key=lambda actividad:convertir_minutos(actividad["hora_inicio"]))

        if actividades_dia:

            print(f"\n{dia}:")

            lineas_mostradas += 1

            for actividad in actividades_dia:

                print(
                    f'- {actividad["materia"]} '
                    f'({actividad["hora_inicio"]} - '
                    f'{actividad["hora_fin"]}) '
                    f'en {actividad["ubicacion"]}'
                )

                lineas_mostradas += 1

                eventos.append({
                    "materia": actividad["materia"],
                    "hora_inicio": actividad["hora_inicio"],
                    "hora_fin": actividad["hora_fin"],
                    "ubicacion": actividad["ubicacion"]
                })

                if lineas_mostradas >= limite_lineas:
                    input("\nPresione ENTER para continuar...")
                    lineas_mostradas = 0

            print("-" * 42)

            reporte.append({"dia": dia,"eventos": eventos})

    with open("reporte_horario.json","w",encoding="utf-8") as archivo:
        json.dump(reporte,archivo,indent=4, ensure_ascii=False)

    print("\nReporte generado y guardado en reporte_horario.json'.\n")

    return True