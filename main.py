import batalla_naval_programacion_lineal as bn
import numpy as np

def cargar_datos_archivo(nombre_archivo):
    """
    Carga los datos de un archivo que contiene:
    - Demandas de filas (n filas).
    - Demandas de columnas (m filas).
    - Largos de los barcos (k filas).
    Los bloques estan separados por lineas en blanco.

    return: Una tupla con (demandas_filas, demandas_columnas, largos_barcos).
    """
    with open(nombre_archivo, 'r') as archivo:
        # Leer todas las lineas del archivo.
        lineas = archivo.readlines()
    
    # Ignorar las dos primeras líneas (comentarios).
    lineas = lineas[2:]

    # Eliminar saltos de linea y lineas en blanco.
    bloques = []
    bloque_actual = []
    for linea in lineas:
        linea = linea.strip()
        if linea == "":  # Separador entre bloques.
            if bloque_actual:  # Si hay datos en el bloque actual.
                bloques.append(bloque_actual)
                bloque_actual = []
        else:
            bloque_actual.append(int(linea))  # Convertir cada linea en numero.
    
    # Agregar el ultimo bloque si no esta vacio.
    if bloque_actual:
        bloques.append(bloque_actual)
    
    # Asignar los bloques segun el formato.
    demandas_filas = bloques[0] if len(bloques) > 0 else []
    demandas_columnas = bloques[1] if len(bloques) > 1 else []
    largos_barcos = bloques[2] if len(bloques) > 2 else []
    
    return demandas_filas, demandas_columnas, largos_barcos


def main():

    archivo_pruebas = ["tests/3_3_2.txt", "tests/5_5_6.txt", "tests/8_7_10.txt", "tests/10_3_3.txt", "tests/10_10_10.txt", "tests/12_12_21.txt", "tests/15_10_15.txt", "tests/20_20_20.txt", "tests/20_25_30.txt", "tests/30_25_25.txt"]
    #for nombre_archivo in archivo_pruebas:
    nombre_archivo = "tests/5_5_6.txt" #input("Ingrese ruta:")
    demandas_filas, demandas_columnas, largos_barcos = cargar_datos_archivo(nombre_archivo)
    print(nombre_archivo + ", greedy_catedra")
    print("Demandas de filas:", demandas_filas)
    print("Demandas de columnas:", demandas_columnas)
    print("Largos de los barcos:", largos_barcos)
     # Convertir las demandas a arrays de NumPy.
    demandas_filas = np.array(demandas_filas)
    demandas_columnas = np.array(demandas_columnas)

    tablero = np.zeros((len(demandas_filas), len(demandas_columnas)), dtype=int)
    #bn.batalla_naval(tablero, largos_barcos, demandas_filas, demandas_columnas)
    demanda, mejor_tablero = bn.batalla_naval(tablero, largos_barcos, demandas_filas, demandas_columnas)

    print(mejor_tablero)
    print(f"Demanda ja: {demanda}")

main()