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
			demandas = demandas_filas_pos if demanda[0] == "f" else demandas_columnas_pos
			demandas_perpendiculares = demandas_columnas_pos if demanda[0] == "f" else demandas_filas_pos
			posicion_posible = obtener_posicion(barco[1], tablero, demanda[1], demanda[0], demandas, demandas_perpendiculares)
			if posicion_posible != -1:
				fila_encontrada = demanda[1] if demanda[0] == "f" else posicion_posible
				columna_encontrada = demanda[1] if demanda[0] == "c" else posicion_posible
				colocar_barco(barco, tablero, demanda[0], fila_encontrada, columna_encontrada)
				demanda[2] -= barco[1]
				reducir_demandas_perpendiculares(posicion_posible, barco[1], demandas_perpendiculares)
				barcos_usados[barco] = True
		
	return (sum(demandas_filas) + sum(demandas_columnas) - devolver_demanda_total_cumplida(demandas_totales)), tablero

def devolver_demanda_total_cumplida(demandas_totales):
	demanda_cumplida = 0
	for info_demanda in demandas_totales:
		demanda_cumplida += info_demanda[2]
	return demanda_cumplida

def obtener_posicion(barco, tablero, pos_demanda, tipo_demanda, demandas, demandas_perpendiculares):

	if demandas[pos_demanda][2] < barco:
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
		if np.all(tablero[max(posicion_fila_inicial, 0): min(posicion_fila_final, limite_filas), max(posicion_columna_inicial, 0): min(posicion_columna_final,limite_columnas)] == 0) and demandas_perpendiculares[posicion_a_probar][2] > 0:
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
	for posicion in range(posicion_a_probar, posicion_a_probar + info_barco[1]):
		fila = fila_a_probar if tipo_demanda == "f" else posicion
		columna = columna_a_probar if tipo_demanda == "c" else posicion
		tablero[fila][columna] = info_barco[0] + 1

def reducir_demandas_perpendiculares(posicion_perpendicular, barco, demandas_perpendiculares):
	for posicion in range(posicion_perpendicular, posicion_perpendicular + barco):
		demandas_perpendiculares[posicion][2] -= 1