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
			if barco in barcos_usados:
				continue
			posicion = encontrar_posicion(tablero, demanda[0], demanda[1], barco[1], demandas_filas_pos, demandas_columnas_pos)
			if posicion != -1:
				demanda[2] -= barco[1]
				for avance in range(posicion, posicion+barco[1]):
					if demanda[0] == "f":
						demandas_columnas_pos[avance][2] -= 1
						tablero[demanda[1]][avance] = barco[0] + 1
					else:
						demandas_filas_pos[avance][2] -= 1
						tablero[avance][demanda[1]] = barco[0] + 1
				barcos_usados[barco] = True

	return (sum(demandas_filas) + sum(demandas_columnas) - devolver_demanda_total_cumplida(demandas_totales)), tablero

def devolver_demanda_total_cumplida(demandas_totales):
	demanda_cumplida = 0
	for info_demanda in demandas_totales:
		demanda_cumplida += info_demanda[2]
	return demanda_cumplida


def encontrar_posicion(tablero, tipo_demanda, pos_demanda, largo_barco, demandas_filas_pos, demandas_columnas_pos):
	espacios_libres_continuos = 0
	if tipo_demanda == "f":
		if demandas_filas_pos[pos_demanda][2] < largo_barco:
			return -1
		for columna in range(len(tablero[pos_demanda])):
			if tablero[pos_demanda][columna] == 0 and demandas_columnas_pos[columna][2] > 0:
				espacios_libres_continuos += 1
			else:
				espacios_libres_continuos = 0
			if espacios_libres_continuos == largo_barco:
				siguiente_columna = columna + 1 if columna + 1 < len(tablero[pos_demanda]) else columna
				columna_anterior = columna - largo_barco if columna - largo_barco >= 0 else columna + 1 - largo_barco
				if tablero[pos_demanda][siguiente_columna] == 0 and tablero[pos_demanda][columna_anterior] == 0:
					return columna + 1 - largo_barco
				espacios_libres_continuos = 0
	else:
		if demandas_columnas_pos[pos_demanda][2] < largo_barco:
			return -1
		for fila in range(len(tablero)):
			if tablero[fila][pos_demanda] == 0  and demandas_filas_pos[fila][2] > 0:
				espacios_libres_continuos += 1
			else:
				espacios_libres_continuos = 0
			if espacios_libres_continuos == largo_barco:
				siguiente_fila = fila + 1 if fila + 1 < len(tablero) else fila
				fila_anterior = fila - largo_barco if fila - largo_barco >= 0 else fila + 1 - largo_barco
				if tablero[siguiente_fila][pos_demanda] == 0 and tablero[fila_anterior][pos_demanda] == 0:
					return fila + 1 - largo_barco
				espacios_libres_continuos = 0
	return -1

def obtener_demanda(info_demanda):
	return info_demanda[2]