from datetime import date
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def leer(nom_arch):
    arch = open(nom_arch, "r")
    arch.seek(0)
    lineas = arch.readlines()
    for linea in lineas:
        datos = linea.split(";")
        largo = 16 - len(datos[0])
        print(f"{datos[0]}{(datos[1][:-1]):>{largo}}")

    arch.close()

def leer_y_obtener_max_score(nom_arch, player):
    scores = [0]
    arch = open(nom_arch, "r")
    arch.seek(0)
    lineas = arch.readlines()
    lineas = lineas[1:]
    for linea in lineas:
        datos = linea.split(";")
        if (datos[2][:-1] == player):
            scores.append(int(datos[1]))

    arch.close()

    return max(scores)

def escribir_titulos(nom_arch):
    arch = open(nom_arch, "w")
    arch.seek(0)
    arch.write("FECHA;SCORE\n")
    arch.close()

def escribir_al_final(nom_arch, score, player):
    arch = open(nom_arch, "a")
    arch.write(f"{date.today()};{score};{player}\n")
    arch.close()

# escribir_titulos("shooter.csv")
# escribir_al_final("shooter.csv", 4)
# leer("shooter.csv")
# print(leer_y_obtener_max_score("shooter.csv"))