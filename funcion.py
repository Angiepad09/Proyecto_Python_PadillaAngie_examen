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
        hora_inicio = input("Ingrese la hora de inicio (Formato 24H, Ejemplo: 14:00)-> ").strip()

        if valida_hora(hora_inicio):
            break
        print("La hora de inicio no es válida.\n")

    while True:
        hora_fin = input("Ingrese la hora de fin (Formato 24H, Ejemplo: 16:00)-> ").strip()

        if not valida_hora(hora_fin):
            print("La hora de fin no es válida.\n")
            continue

        if not rango_hora(hora_inicio, hora_fin):
            print("La hora de fin debe ser mayor que la hora de inicio.\n")
            continue
        break
    
    ubicacion = input("Ingrese la ubicacion (Presione ENTER para omitir)->").strip().capitalize()

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
        f"| {'Miercoles':<15}"
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
        nueva_hora_inicio = input("Ingrese la nueva hora de inicio (Formato 24H - Ejemplo: 14:00)-> ").strip()

        if valida_hora(nueva_hora_inicio):
            break

        print("La hora de inicio ingresada no es válida. Intente de nuevo.\n")

    while True:
        nueva_hora_fin = input("Ingrese la nueva hora de fin (Formato 24H - Ejemplo: 16:00)-> ").strip()

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
        dia = input("Ingrese el día de la semana (Lunes, Martes, Miercoles, Jueves, Viernes)-> ").strip().capitalize()

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

###################################################################################################
def buscar_actividad():
    horario = cargar_horario()

    if not horario:
        print("No hay actividades registradas.\n")
        return False
    print("-------------- Busqueda por: --------------")
    print("1.Buscar por actividad\n2.Buscar por dia\n3.Buscar por ubicacion\n4.Buscar por hora")
    
    try:
        opcion_submenu=int(input("Seleccione una opcion (ejemplo 1)->"))
        print()
    except ValueError:
        print("Opcion no valida, debe digitar numeros")
        return
        
    encontrados=[]
     
        
    if opcion_submenu==1:
        
        materia = input("Ingrese el nombre de la materia o actividad que desea buscar-> ").strip().capitalize()
        for actividad in horario:
            if actividad["materia"] == materia:
                encontrados.append(actividad)
                
    elif opcion_submenu==2:
        
        dia = input("Ingrese el día que desea buscar -> ").strip().capitalize()

        if not validar_dia(dia):
            print("El día ingresado no es válido.\n")
            return

        for actividad in horario:
            if actividad["dia"] == dia:
                encontrados.append(actividad)

        if not encontrados:
            print(f"El día {dia} está libre.\n")
            return
                                
    elif opcion_submenu==3:
        
        ubicacion= input("Ingrese la ubicacion que buscar-> ").strip().capitalize()
        for actividad in horario:
            if actividad["ubicacion"] == ubicacion:
                encontrados.append(actividad)
                
    elif opcion_submenu == 4:
        hora = input("Ingrese la hora (Formato 24H - Ejemplo: 14:00) -> ").strip()

        if not valida_hora(hora):
            print("La hora ingresada no es válida. Intente de nuevo.\n")
            return

        for actividad in horario:

            inicio = convertir_minutos(actividad["hora_inicio"])
            fin = convertir_minutos(actividad["hora_fin"])
            hora_buscada = convertir_minutos(hora)
            if inicio <= hora_buscada < fin:
                encontrados.append(actividad)
        if not encontrados:
            print(f"No hay actividades registradas a las {hora}.\n")
            return

    else: 
            print("Opcion no valida, intente de nuevo")
            return
        
    if not encontrados:
        print(f'No se pudo encontrar porque no existe.\n')
        
    for actividad in encontrados:
        print(f'Materia: {actividad["materia"]}\nDía: {actividad["dia"]}\nHorario: {actividad["hora_inicio"]} - {actividad["hora_fin"]}\nUbicación: {actividad["ubicacion"]}\n')
      
    with open("resultado_busqueda.json","w",encoding="utf-8") as archivo:
        json.dump(encontrados,archivo,indent=4,ensure_ascii=False)

    print("Resultados guardados en resultado_busqueda.json")
###################################################################################################
def estadistica():

    horario = cargar_horario()

    if not horario:
        print("No hay actividades regi  stradas.\n")
        return
    
    cantidad_actividad=len(horario)
    total_horas = 0
    

    dias = {
        "Lunes": 0,
        "Martes": 0,
        "Miercoles": 0,
        "Jueves": 0,
        "Viernes": 0
    }
    

    for actividad in horario:

        inicio = convertir_minutos(actividad["hora_inicio"])
        fin = convertir_minutos(actividad["hora_fin"])

        duracion = (fin - inicio) / 60
        total_horas += duracion
        dias[actividad["dia"]] += duracion
        
    dias_con_actividades = sum(1 for horas in dias.values() if horas > 0)
    dia_mas_ocupado = max(dias, key=dias.get)
    dia_menos_ocupado = min(dias, key=dias.get)
    
    if dias_con_actividades > 0:        
        promedio = total_horas / dias_con_actividades
    else:
        promedio = 0
        
    estadisticas = {
        "cantidad_actividades": cantidad_actividad,
        "horas_programadas": total_horas,
        "dia_mas_ocupado": dia_mas_ocupado,
        "horas_dia_mas_ocupado": dias[dia_mas_ocupado],
        "dia_menos_ocupado": dias[dia_menos_ocupado],
        "promedio":promedio
        }
    
    with open("estadisticas.json", "w", encoding="utf-8") as archivo:
        json.dump(estadisticas,archivo,indent=4,ensure_ascii=False)

    print("\n" + "=" * 40)
    print("ESTADISTICAS DEL HORARIO")
    print("=" * 40)
    print(f"Total de actividades: {cantidad_actividad}")
    print(f"Horas programadas: {total_horas:.1f}")
    print(f"Dia mas ocupado: {dia_mas_ocupado} con {dias[dia_mas_ocupado]:.1f} horas")
    print(f"Dia menos ocupado: {dia_menos_ocupado} con {dias[dia_menos_ocupado]:.1f} horas")
    print(f"Promedio diario: {promedio:.1f} horas")
    
    print("\nHoras por día:")

    for dia, horas in dias.items():
        print(f"{dia}: {horas:.1f} horas")

###################################################################################################
def buscar_espacios_libres():

    horario = cargar_horario()

    while True:
        dia = input("Ingrese el día que desea consultar (Lunes, Martes, Miercoles, Jueves, Viernes)-> ").strip().capitalize()

        if validar_dia(dia):
            break
        print("El día ingresado no es válido. Intente de nuevo.\n")

    while True:
        hora_desde = input("Ingrese hora inicial de consulta (Formato 24H, Ejemplo: 08:00)-> ").strip()

        if valida_hora(hora_desde):
            break
        print("La hora ingresada no es válida. Intente de nuevo.\n")

    while True:
        hora_hasta = input("Ingrese hora final de consulta (Formato 24H, Ejemplo: 18:00)-> ").strip()

        if not valida_hora(hora_hasta):
            print("La hora ingresada no es válida. Intente de nuevo.\n")
            continue

        if not rango_hora(hora_desde, hora_hasta):
            print("La hora final debe ser mayor que la hora inicial. Intente de nuevo.\n")
            continue
        break

    actividades_dia = [actividad for actividad in horario if actividad["dia"] == dia]
    actividades_dia.sort(key=lambda actividad: convertir_minutos(actividad["hora_inicio"]))

    inicio_consulta = convertir_minutos(hora_desde)
    fin_consulta = convertir_minutos(hora_hasta)

    def formato(minutos):
        return f"{minutos // 60:02d}:{minutos % 60:02d}"

    espacios_libres = []
    actual = inicio_consulta

    for actividad in actividades_dia:

        inicio_actividad = convertir_minutos(actividad["hora_inicio"])
        fin_actividad = convertir_minutos(actividad["hora_fin"])

        if inicio_actividad >= fin_consulta:
            break

        if fin_actividad <= inicio_consulta:
            continue

        if inicio_actividad > actual:
            espacios_libres.append((actual, min(inicio_actividad, fin_consulta)))

        if fin_actividad > actual:
            actual = fin_actividad

    if actual < fin_consulta:
        espacios_libres.append((actual, fin_consulta))

    print("\n" + "=" * 42)
    print(f"ESPACIOS LIBRES DEL {dia.upper()}")
    print("=" * 42)

    if not espacios_libres:
        print("No hay espacios libres disponibles en ese rango.\n")
        return

    for inicio, fin in espacios_libres:
        print(f"{formato(inicio)} - {formato(fin)}")
    print()

###################################################################################################
def sugerir_horario():

    horario = cargar_horario()

    while True:
        dia = input("Ingrese el día de la actividad (Lunes, Martes, Miercoles, Jueves, Viernes)-> ").strip().capitalize()

        if validar_dia(dia):
            break
        print("El día ingresado no es válido. Intente de nuevo.\n")

    while True:
        try:
            duracion_horas = float(input("Ingrese la duración de la actividad en horas (Ejemplo: 2)-> "))
            if duracion_horas > 0:
                break
            print("La duración debe ser mayor que cero. Intente de nuevo.\n")
        except ValueError:
            print("Debe ingresar un número. Intente de nuevo.\n")

    while True:
        hora_desde = input("Ingrese la hora desde la cual puede programarse (Formato 24H, Ejemplo: 08:00)-> ").strip()

        if valida_hora(hora_desde):
            break
        print("La hora ingresada no es válida. Intente de nuevo.\n")

    while True:
        hora_hasta = input("Ingrese la hora máxima hasta la cual puede programarse (Formato 24H, Ejemplo: 18:00)-> ").strip()

        if not valida_hora(hora_hasta):
            print("La hora ingresada no es válida. Intente de nuevo.\n")
            continue

        if not rango_hora(hora_desde, hora_hasta):
            print("La hora final debe ser mayor que la hora inicial. Intente de nuevo.\n")
            continue
        break

    actividades_dia = [actividad for actividad in horario if actividad["dia"] == dia]
    actividades_dia.sort(key=lambda actividad: convertir_minutos(actividad["hora_inicio"]))

    inicio_busqueda = convertir_minutos(hora_desde)
    fin_busqueda = convertir_minutos(hora_hasta)
    duracion_minutos = int(duracion_horas * 60)

    def formato(minutos):
        return f"{minutos // 60:02d}:{minutos % 60:02d}"

    espacios_libres = []
    actual = inicio_busqueda

    for actividad in actividades_dia:

        inicio_actividad = convertir_minutos(actividad["hora_inicio"])
        fin_actividad = convertir_minutos(actividad["hora_fin"])

        if inicio_actividad >= fin_busqueda:
            break

        if fin_actividad <= inicio_busqueda:
            continue

        if inicio_actividad > actual:
            espacios_libres.append((actual, min(inicio_actividad, fin_busqueda)))

        if fin_actividad > actual:
            actual = fin_actividad

    if actual < fin_busqueda:
        espacios_libres.append((actual, fin_busqueda))

    horarios_disponibles = []

    for inicio, fin in espacios_libres:
        inicio_slot = inicio
        while inicio_slot + duracion_minutos <= fin:
            horarios_disponibles.append((inicio_slot, inicio_slot + duracion_minutos))
            inicio_slot += duracion_minutos

    print("\n" + "=" * 42)
    print("HORARIOS DISPONIBLES")
    print("=" * 42)

    if not horarios_disponibles:
        print(f"No existen espacios disponibles para una actividad de esa duración.\n")
        return

    for numero, (inicio, fin) in enumerate(horarios_disponibles, start=1):
        print(f"{numero}. {formato(inicio)} - {formato(fin)}")
    print()
    
###############################################################################

def calcular_duracion():

    horario = cargar_horario()

    if not horario:
        print("No hay actividades registradas.\n")
        return

    for actividad in horario:

        inicio = convertir_minutos(
            actividad["hora_inicio"]
        )

        fin = convertir_minutos(
            actividad["hora_fin"]
        )

        duracion = fin - inicio

        horas = duracion // 60
        minutos = duracion % 60

        print(
            f"\nMateria: {actividad['materia']}"
        )

        print(
            f"Duracion: {horas} hora(s) "
            f"y {minutos} minuto(s)"
        )

###############################################################################################

def espacios_libres():

    horario = cargar_horario()

    if not horario:
        print("No hay actividades registradas.\n")
        return

    dias = [
        "Lunes",
        "Martes",
        "Miercoles",
        "Jueves",
        "Viernes"
    ]

    inicio_jornada = "06:00"
    fin_jornada = "22:00"

    for dia in dias:

        actividades_dia = []

        for actividad in horario:

            if actividad["dia"] == dia:
                actividades_dia.append(actividad)

        actividades_dia.sort(
            key=lambda x:
            convertir_minutos(x["hora_inicio"])
        )

        print(f"\n=== {dia} ===")

        if not actividades_dia:
            print("Dia completamente libre.")
            continue

        hora_actual = inicio_jornada

        for actividad in actividades_dia:

            if convertir_minutos(hora_actual) < convertir_minutos(actividad["hora_inicio"]):

                print(
                    f"Libre de {hora_actual} "
                    f"a {actividad['hora_inicio']}"
                )

            hora_actual = actividad["hora_fin"]

        if convertir_minutos(hora_actual) < convertir_minutos(fin_jornada):

            print(
                f"Libre de {hora_actual} "
                f"a {fin_jornada}"
            )
########################################################################################################################

def contar_por_dia():

    horario = cargar_horario()

    if not horario:
        print("No hay actividades registradas.\n")
        return

    dias = [
        "Lunes",
        "Martes",
        "Miercoles",
        "Jueves",
        "Viernes"
    ]

    print("\nRESUMEN POR DIA")
    print("-" * 40)

    for dia in dias:

        contador = 0
        horas_totales = 0

        for actividad in horario:

            if actividad["dia"] == dia:

                contador += 1

                inicio = convertir_minutos(
                    actividad["hora_inicio"]
                )

                fin = convertir_minutos(
                    actividad["hora_fin"]
                )

                horas_totales += (fin - inicio) / 60

        print(
            f"{dia}: "
            f"{contador} actividad(es) - "
            f"{horas_totales:.1f} hora(s)"
        )
        
##############################################################################################################    
    

    
    