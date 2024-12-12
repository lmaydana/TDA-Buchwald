import numpy as np
def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
	demandas_columnas_pos = [["c", i, demandas_columnas[i]] for i in range(len(demandas_columnas))]
	demandas_filas_pos= [["f", i, demandas_filas[i]] for i in range(len(demandas_filas))]
	demandas_totales = demandas_columnas_pos + demandas_filas_pos
	demandas_totales.sort(key=lambda demanda: demanda[2]*(-1))
	barcos_aux = [(n, barcos[n]) for n in range(len(barcos))]
	barcos_aux.sort(key=lambda numero_largo_barco: numero_largo_barco[1]*(-1))
	barcos_usados = {}
	for demanda in demandas_totales:
		for barco in barcos_aux:
			if barco in barcos_usados or barco[1] > demanda[2]:
				continue
			posicion_perpendicular_maxima = len(demandas_columnas) if demanda[0] == "f" else len(demandas_filas)
			for posicion_posible in range(posicion_perpendicular_maxima):
				fila_a_probar = demanda[1] if demanda[0] == "f" else posicion_posible
				columna_a_probar = demanda[1] if demanda[0] == "c" else posicion_posible
				demandas = demandas_filas_pos if demanda[0] == "f" else demandas_columnas_pos
				demandas_perpendiculares = demandas_columnas_pos if demanda[0] == "f" else demandas_filas_pos
				if entra_barco(barco[1], tablero, fila_a_probar, columna_a_probar, demanda[0], demanda[1], demandas, demandas_perpendiculares):
					colocar_barco(barco, tablero, demanda[0], fila_a_probar, columna_a_probar)
					demanda[2] -= barco[1]
					reducir_demandas_perpendiculares(posicion_posible, barco[1], demandas_perpendiculares)
					barcos_usados[barco] = True
					break
		
	return (sum(demandas_filas) + sum(demandas_columnas) - devolver_demanda_total_cumplida(demandas_totales)), tablero

def devolver_demanda_total_cumplida(demandas_totales):
	demanda_cumplida = 0
	for info_demanda in demandas_totales:
		demanda_cumplida += info_demanda[2]
	return demanda_cumplida

def entra_barco(barco, tablero, fila_a_probar, columna_a_probar, tipo_demanda, pos_demanda, demandas, demandas_perpendiculares):
	if demandas[pos_demanda][2] < barco:
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
		if demandas[pos][2] <= 0:
			return False
	return True

def colocar_barco(info_barco, tablero, tipo_demanda, fila_a_probar, columna_a_probar):
	posicion_a_probar = fila_a_probar if tipo_demanda == "c" else columna_a_probar
	for posicion in range(posicion_a_probar, posicion_a_probar + info_barco[1]):
		fila = fila_a_probar if tipo_demanda == "f" else posicion
		columna = columna_a_probar if tipo_demanda == "c" else posicion
		tablero[fila][columna] = info_barco[0] + 1

def reducir_demandas_perpendiculares(posicion_perpendicular, barco, demandas_perpendiculares):
	for posicion in range(posicion_perpendicular, posicion_perpendicular + barco):
		demandas_perpendiculares[posicion][2] -= 1