def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
	demandas_columnas_pos = [["c", i, demandas_columnas[i]] for i in range(len(demandas_columnas))]
	demandas_filas_pos= [["f", i, demandas_filas[i]] for i in range(len(demandas_filas))]
	demandas_totales = demandas_columnas_pos + demandas_filas_pos
	demandas_totales.sort(key=obtener_demanda)
	barcos_aux = [(n, barcos[n]) for n in range(len(barcos))]
	barcos_aux.sort(key=lambda numero_largo_barco: numero_largo_barco[1]*(-1))
	while barcos_aux and existe_barco_que_entre_en_demanda(tablero, demandas_filas_pos, demandas_columnas_pos, demandas_totales, barcos_aux):
		info_demanda = max(demandas_totales, key=obtener_demanda)
		tipo_demanda = info_demanda[0]
		pos_demanda = info_demanda[1]
		cantidad_demanda = info_demanda[2]
		pos_barco = 0
		while pos_barco < len(barcos_aux) and (barcos_aux[pos_barco][1] > cantidad_demanda or barcos_aux[pos_barco][1] > maxima_cantidad_de_contiguos_disponibles(tablero, tipo_demanda, pos_demanda, demandas_filas_pos, demandas_columnas_pos)):
			pos_barco += 1
		
		if pos_barco >= len(barcos_aux):
		    demandas_totales.remove(info_demanda)
		    continue
		largo_barco = barcos_aux[pos_barco][1]
		posicion = encontrar_posicion(tablero, tipo_demanda, pos_demanda, largo_barco , demandas_filas_pos, demandas_columnas_pos)
		if tipo_demanda == "f":
			for j in range(largo_barco):
				tablero[pos_demanda][posicion + j] = barcos_aux[pos_barco][0] + 1
				demandas_columnas_pos[posicion + j][2] -= 1
		else:
			for j in range(largo_barco):
				tablero[posicion + j][pos_demanda] = barcos_aux[pos_barco][0] + 1
				demandas_filas_pos[posicion + j][2] -= 1
		barcos_aux.pop(pos_barco)
		info_demanda[2] -= largo_barco
	return devolver_demanda_total_cumplida(demandas_totales), tablero

def devolver_demanda_total_cumplida(demandas_totales):
	demanda_cumplida = 0
	for info_demanda in demandas_totales:
		demanda_cumplida += info_demanda[2]
	return demanda_cumplida


def existe_barco_que_entre_en_demanda(tablero, demandas_filas_pos, demandas_columnas_pos, demandas_totales, barcos_aux):
	demandas_totales_aux = demandas_totales.copy()
	demandas_totales_aux.sort(key=obtener_demanda)
	demandas_totales_aux.reverse()
	largo_barco_mas_chico = barcos_aux[-1][1]
	for demanda in demandas_totales_aux:
		if demanda[0] == "f" and demandas_filas_pos[demanda[1]][2] < largo_barco_mas_chico or demanda[0] == "c" and demandas_columnas_pos[demanda[1]][2] < largo_barco_mas_chico:
			return False
		if encontrar_posicion(tablero, demanda[0], demanda[1], largo_barco_mas_chico, demandas_filas_pos, demandas_columnas_pos) != -1:
			return True 
	return False

def obtener_suma_demanda(demandas):
	suma = 0
	for info_demanda in demandas:
		suma += info_demanda[2]
	return suma

def encontrar_posicion(tablero, tipo_demanda, pos_demanda, largo_barco, demandas_filas_pos, demandas_columnas_pos):
	espacios_libres_continuos = 0
	if tipo_demanda == "f":
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
		for fila in range(len(tablero)):
			if tablero[fila][pos_demanda] == 0  and demandas_filas_pos[fila][2] > 0:
				espacios_libres_continuos += 1
			else:
				espacios_libres_continuos = 0
			if espacios_libres_continuos == largo_barco:
				siguiente_fila = fila + 1 if fila + 1 < len(tablero[pos_demanda]) else fila
				fila_anterior = fila - largo_barco if fila - largo_barco >= 0 else fila + 1 - largo_barco
				if tablero[siguiente_fila][pos_demanda] == 0 and tablero[fila_anterior][pos_demanda] == 0:
					return fila + 1 - largo_barco
				espacios_libres_continuos = 0
	return -1

def maxima_cantidad_de_contiguos_disponibles(tablero, tipo_demanda, pos_demanda, demandas_filas_pos, demandas_columnas_pos):
	maximos_espacios_libres = 0
	espacios_libres_continuos = 0
	if tipo_demanda == "f":
		for columna in range(len(tablero[pos_demanda])):
			if tablero[pos_demanda][columna] == 0 and demandas_columnas_pos[columna][2] > 0:
				espacios_libres_continuos += 1
			else:
				espacios_libres_continuos = 0
			siguiente_columna = columna + 1 if columna + 1 < len(tablero[pos_demanda]) else columna
			columna_anterior = columna - espacios_libres_continuos if columna - espacios_libres_continuos >= 0 else columna + 1 - espacios_libres_continuos
			if tablero[pos_demanda][siguiente_columna] == 0 or tablero[pos_demanda][columna_anterior] == 0:
				if maximos_espacios_libres < espacios_libres_continuos:
					maximos_espacios_libres = espacios_libres_continuos
			else:
				espacios_libres_continuos = 0
	else:
		for fila in range(len(tablero)):
			if tablero[fila][pos_demanda] == 0  and demandas_filas_pos[fila][2] > 0:
				espacios_libres_continuos += 1
			else:
				espacios_libres_continuos = 0
			siguiente_fila = fila + 1 if fila + 1 < len(tablero) else fila
			fila_anterior = fila - espacios_libres_continuos if fila - espacios_libres_continuos >= 0 else fila + 1 - espacios_libres_continuos
			if tablero[siguiente_fila][pos_demanda] == 0 and tablero[fila_anterior][pos_demanda] == 0:
				if espacios_libres_continuos > maximos_espacios_libres:
					maximos_espacios_libres = espacios_libres_continuos
			else:
				espacios_libres_continuos = 0
	return maximos_espacios_libres

def obtener_demanda(info_demanda):
	return info_demanda[2]