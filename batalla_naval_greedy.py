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
		casilleros_a_probar = len(demandas_filas) if tipo_demanda == "c" else len(demandas_columnas)
		for indice_barco in indices_disponibles:
			info_barco = barcos_aux[indice_barco]
			barco = info_barco[LARGO_BARCO]
			for celda in range(casilleros_a_probar - barco + 1):
				fila_a_probar = pos_demanda if tipo_demanda == "f" else celda
				columna_a_probar = pos_demanda if tipo_demanda == "c" else celda
				demandas = demandas_columnas_pos if tipo_demanda == "c" else demandas_filas_pos
				demandas_perpendiculares = demandas_filas_pos if tipo_demanda == "c" else demandas_columnas_pos
				if entra_barco(barco, tablero, fila_a_probar, columna_a_probar, tipo_demanda, pos_demanda, demandas, demandas_perpendiculares):
					colocar_barco(info_barco, tablero, tipo_demanda, fila_a_probar, columna_a_probar)
					info_demanda[CANTIDAD_DEMANDA] -= barco
					reducir_demandas_perpendiculares(celda, barco, demandas_perpendiculares)
					heapq.heappush(demandas_totales, info_demanda)
					heapq._heapify_max(demandas_totales)
					indices_disponibles.pop(indice_barco)
					break
			if indice_barco not in indices_disponibles:
				break
			indice_barco += 1

	return (sum(demandas_filas) + sum(demandas_columnas) - devolver_demanda_total_cumplida(demandas_filas_pos) - devolver_demanda_total_cumplida(demandas_columnas_pos)), tablero

def entra_barco(barco, tablero, fila_a_probar, columna_a_probar, tipo_demanda, pos_demanda, demandas, demandas_perpendiculares):
	if demandas[pos_demanda][CANTIDAD_DEMANDA] < barco:
		return False
	if tipo_demanda == "c" and fila_a_probar + barco > len(demandas_perpendiculares) or tipo_demanda == "f" and columna_a_probar + barco > len(demandas_perpendiculares):
		return False
	if tipo_demanda == "c" and not np.all(tablero[max(fila_a_probar - 1, 0): min(fila_a_probar + barco + 1, len(demandas_perpendiculares)), max(columna_a_probar - 1, 0): min(columna_a_probar + 2, len(demandas))] == 0) or tipo_demanda == "f" and not np.all(tablero[max(0, fila_a_probar - 1): min(fila_a_probar + 2, len(demandas)), max(0, columna_a_probar - 1): min(columna_a_probar + barco + 1, len(demandas_perpendiculares))] == 0):
		return False

	if tipo_demanda == "c" and not son_todas_las_demandas_contiguas_positivas(fila_a_probar, barco, demandas_perpendiculares) or tipo_demanda == "f" and not son_todas_las_demandas_contiguas_positivas(columna_a_probar, barco, demandas_perpendiculares):
		return False
	
	return True

def son_todas_las_demandas_contiguas_positivas(posicion, barco, demandas):
	for pos in range(posicion, min(posicion + barco, len(demandas))):
		if demandas[pos][CANTIDAD_DEMANDA] <= 0:
			return False
	return True

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