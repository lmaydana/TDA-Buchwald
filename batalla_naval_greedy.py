import  heapq
import numpy as np
CANTIDAD_DEMANDA = 0
TIPO_DEMANDA = 1
POSICION_DEMANDA = 2
INDICE_BARCO = 0
LARGO_BARCO = 1
def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
	demandas_columnas_pos = [[demandas_columnas[i], "c", i ] for i in range(len(demandas_columnas))]
	demandas_filas_pos= [[demandas_filas[i], "f", i ] for i in range(len(demandas_filas))]
	demandas_totales = demandas_columnas_pos + demandas_filas_pos
	heapq._heapify_max(demandas_totales)
	barcos_aux = [(n, barcos[n]) for n in range(len(barcos))]
	barcos_aux.sort(key=lambda numero_largo_barco: numero_largo_barco[1]*(-1))
	indices_disponibles = {i: True for i in range(len(barcos_aux))}
	while indices_disponibles and demandas_totales:
		indice_barco = 0
		info_demanda = heapq._heappop_max(demandas_totales)
		tipo_demanda = info_demanda[TIPO_DEMANDA]
		pos_demanda = info_demanda[POSICION_DEMANDA]
		for indice_barco in indices_disponibles:
			info_barco = barcos_aux[indice_barco]
			barco = info_barco[LARGO_BARCO]
			demandas = demandas_columnas_pos if tipo_demanda == "c" else demandas_filas_pos
			demandas_perpendiculares = demandas_filas_pos if tipo_demanda == "c" else demandas_columnas_pos
			celda = obtener_posicion(barco, tablero, pos_demanda, tipo_demanda, demandas, demandas_perpendiculares)
			if celda != -1:
				fila_encontrada = pos_demanda if tipo_demanda == "f" else celda
				columna_encontrada = pos_demanda if tipo_demanda == "c" else celda
				colocar_barco(info_barco, tablero, tipo_demanda, fila_encontrada, columna_encontrada)
				info_demanda[CANTIDAD_DEMANDA] -= barco
				reducir_demandas_perpendiculares(celda, barco, demandas_perpendiculares)
				heapq.heappush(demandas_totales, info_demanda)
				heapq._heapify_max(demandas_totales)
				indices_disponibles.pop(indice_barco)
				break

	return (sum(demandas_filas) + sum(demandas_columnas) - devolver_demanda_total_cumplida(demandas_filas_pos) - devolver_demanda_total_cumplida(demandas_columnas_pos)), tablero

def obtener_posicion(barco, tablero, pos_demanda, tipo_demanda, demandas, demandas_perpendiculares):

	if demandas[pos_demanda][CANTIDAD_DEMANDA] < barco:
		return -1
	contiguos_disponibles = 0
	posicion_contiguos = -1
	for posicion_a_probar in range(len(demandas_perpendiculares)):
		if posicion_contiguos + barco > len(demandas_perpendiculares):
			return -1
		posicion_fila_inicial = (posicion_a_probar if tipo_demanda == "c" else pos_demanda) - 1
		posicion_fila_final = (posicion_a_probar if tipo_demanda == "c" else pos_demanda) + 2
		posicion_columna_inicial = (pos_demanda if tipo_demanda == "c" else posicion_a_probar) - 1
		posicion_columna_final = (pos_demanda if tipo_demanda == "c" else posicion_a_probar) + 2
		limite_filas = len(demandas) if tipo_demanda == "f" else len(demandas_perpendiculares)
		limite_columnas = len(demandas_perpendiculares) if tipo_demanda == "f" else len(demandas)
		if np.all(tablero[max(posicion_fila_inicial, 0): min(posicion_fila_final, limite_filas), max(posicion_columna_inicial, 0): min(posicion_columna_final,limite_columnas)] == 0) and demandas_perpendiculares[posicion_a_probar][CANTIDAD_DEMANDA] > 0:
			if contiguos_disponibles == 0:
				posicion_contiguos = posicion_a_probar
			contiguos_disponibles += 1
		else:
			posicion_contiguos = -1
			contiguos_disponibles = 0
		if contiguos_disponibles == barco:
			return posicion_contiguos
	return -1

def colocar_barco(info_barco, tablero, tipo_demanda, fila_a_probar, columna_a_probar):
	posicion_a_probar = fila_a_probar if tipo_demanda == "c" else columna_a_probar
	for posicion in range(posicion_a_probar, posicion_a_probar + info_barco[LARGO_BARCO]):
		fila = fila_a_probar if tipo_demanda == "f" else posicion
		columna = columna_a_probar if tipo_demanda == "c" else posicion
		tablero[fila][columna] = info_barco[INDICE_BARCO] + 1


def reducir_demandas_perpendiculares(posicion_perpendicular, barco, demandas_perpendiculares):
	for posicion in range(posicion_perpendicular, posicion_perpendicular + barco):
		demandas_perpendiculares[posicion][CANTIDAD_DEMANDA] -= 1

def devolver_demanda_total_cumplida(demandas_totales):
	demanda_cumplida = 0
	for info_demanda in demandas_totales:
		demanda_cumplida += info_demanda[CANTIDAD_DEMANDA]
	return demanda_cumplida