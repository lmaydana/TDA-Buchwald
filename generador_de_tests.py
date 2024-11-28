import numpy as np
import random

random.seed(123)
def generador_de_test_con_optimo(n, m, cant_barcos):
	tablero = np.zeros((n, m), dtype=int)
	espacios_disponibles = {k:True for k in range(n*m)}
	barcos = [random.randint(1, min(n, m) + 1) for _ in range(cant_barcos)]
	barcos_final = []
	while espacios_disponibles and barcos:
		barco = barcos.pop()
		posiciones_disponibles = espacios_disponibles.keys()
		for posicion_disponible in posiciones_disponibles:
			if puedo_colocar(barco, posicion_disponible, posiciones_disponibles, "H", m, n):
				colocar(barco, posicion_disponible, tablero, "H", espacios_disponibles, m)
				break
			if puedo_colocar(barco, posicion_disponible, posiciones_disponibles, "V", m, n):
				colocar(barco, posicion_disponible, tablero, "V", espacios_disponibles, m)
				break
		barcos_final.append(barco)
	demandas_filas = []
	for fila in tablero:
		demandas_filas.append(sum(fila))

	demandas_columnas = []

	for columna in range(m):
		demandas_columnas.append(sum([1 for fila in range(n) if tablero[fila][columna] != 0]))

	optimo = sum(demandas_filas) + sum(demandas_columnas)
	escribir_archivo(demandas_filas, demandas_columnas, barcos_final)
	return tablero, barcos_final, demandas_filas, demandas_columnas, optimo

def escribir_archivo(demandas_filas, demandas_columnas, barcos):
	archivo = open(f"tests/{len(demandas_filas)}_{len(demandas_columnas)}_{len(barcos)}.txt", "w")
	archivo.write(f"# El archivo tiene n filas con las demandas de las filas, luego m filas con las demandas de las columnas\n")
	archivo.write("# y luego k filas con el largo de los barcos, separadas por una línea en blanco\n")
	#archivo.write("\n")
	lista_demandas_filas = np.char.mod('%d',demandas_filas)
	archivo.write('\n'.join(lista_demandas_filas))
	archivo.write("\n")
	archivo.write("\n")
	lista_demandas_columnas = np.char.mod('%d',demandas_columnas)
	archivo.write('\n'.join(lista_demandas_columnas))
	archivo.write("\n")
	archivo.write("\n")
	lista_barcos = np.char.mod('%d',barcos)
	archivo.write('\n'.join(lista_barcos))
	archivo.write("\n")
	archivo.close()

def puedo_colocar(barco, posicion_disponible, posiciones_disponibles, orientacion, m, n):
    """
    Verifica si es posible colocar un barco en cualquier dirección (derecha/izquierda o abajo/arriba)
    respetando las restricciones de:
    - Adyacencia.
    - Demandas de filas y columnas.
    """
    fila = posicion_disponible//m
    columna = posicion_disponible % m
    if orientacion == "H":
        if columna + barco > m:
            return False
        if not all((fila*m + pos_col) in posiciones_disponibles for pos_col in range(columna, columna + barco)):
        	return False
    else:
        if fila + barco > n:
            return False
        if not all((pos_fila*m + columna) in posiciones_disponibles for pos_fila in range(fila, fila + barco)):
        	return False

    return True

def colocar(barco, posicion_disponible, tablero, orientacion, posiciones_disponibles, m):
	fila = posicion_disponible//m
	columna = posicion_disponible % m
	if orientacion == "H":
		for pos_columna in range(columna, columna + barco):
			tablero[fila][pos_columna] = 1
		for pos_fila in range(max(0, fila - 1), min(fila + 2, len(tablero))):
			for pos_columna in range(max(0, columna - 1), min(columna + barco + 1, len(tablero[pos_fila]))):
				posiciones_disponibles.pop(pos_fila*m + pos_columna, None)
	else:
		for pos_fila in range(fila, fila + barco):
			tablero[pos_fila][columna] = 1
		for pos_fila in range(max(0, fila - 1), min(fila + barco + 1, len(tablero))):
			for pos_columna in range(max(0, columna - 1), min(columna + 2, len(tablero[pos_fila]))):
				posiciones_disponibles.pop(pos_fila*m + pos_columna, None)