
from funcion import *

horario_semanal=[]

while True:
    
    try:
        print("-------------- Menu --------------")
        print("1.Registrar una materia o actividad\n2.Ver horario semanal\n3.Modificar una materia o actividad\n4.Eliminar una materia o actividad\n5.Generar reporte del horario\n6.Salir")
        opcion_menu=int(input("Seleccione una opcion (ejemplo 1)->"))
        if opcion_menu==6:
            print("Vuelva Pronto\nSaliendo")
            break
        elif opcion_menu==1:
            registrar_actividad(horario_semanal)

        elif opcion_menu==2:
            mostrar_horario()

        elif opcion_menu==3:
            modificar_actividad()

        elif opcion_menu==4:
            eliminar_actividad()

        elif opcion_menu==5:
            generar_reporte()
##################################################################################            
        elif opcion_menu==7:
            buscar_actividad() 
           
            
            
##################################################################################            
        else:
            print("Las opciones del menu estan entre 1 al 6. Intente de Nuevo\n")

    except ValueError:
        print("Las opciones de menu son con numeros. Intente de Nuevo\n")
        