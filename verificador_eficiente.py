NUMERO_BARCO = 0
POSICION_EXTREMO_INICIAL = 1
POSICION_EXTREMO_FINAL = 2
FILA = 0
COLUMNA = 1
def verificador_eficiente(tablero, barcos, demanda_fila, demanda_columna):
	solucion = []
	barcos_colocados = {}

	for fila_pos in range(len(tablero)):
		fila = tablero[fila_pos]
		for celda_pos in range(len(fila)):
			celda = fila[celda_pos]
			if celda != 0:
				barcos_colocados[celda] = barcos_colocados.get(celda, []) + [(fila_pos, celda_pos)]
	barcos_copia = barcos.copy()
	for clave in barcos_colocados:
		pos_extremo_inicial = barcos_colocados[clave][0]
		pos_extremo_final = barcos_colocados[clave][-1]
		diferencia_fila = pos_extremo_final[FILA] - pos_extremo_inicial[FILA]
		diferencia_columna = pos_extremo_final[COLUMNA] - pos_extremo_inicial[COLUMNA]
		if diferencia_fila != 0 and diferencia_columna != 0:
			return False
		largo_barco = max(diferencia_fila, diferencia_columna) + 1
		if largo_barco != barcos[clave - 1]:
			return False
		solucion.append((clave - 1, barcos_colocados[clave][0], barcos_colocados[clave][-1]))


	return verificar_solucion(barcos, demanda_fila, demanda_columna, solucion)

def verificar_solucion(barcos, demanda_fila, demanda_columna, solucion):
	casilleros_ocupados = {}
	demanda_fila_incumplida = demanda_fila.copy()
	demanda_columna_incumplida = demanda_columna.copy()
	for barco_posicion in solucion:
		pos_extremo_inicial = barco_posicion[POSICION_EXTREMO_INICIAL]
		pos_extremo_final = barco_posicion[POSICION_EXTREMO_FINAL]
		diferencia_fila = pos_extremo_final[FILA] - pos_extremo_inicial[FILA]
		diferencia_columna = pos_extremo_final[COLUMNA] - pos_extremo_inicial[COLUMNA]
		if not estan_todos_los_casilleros_disponibles(pos_extremo_inicial, pos_extremo_final, casilleros_ocupados):
			return False
		largo_barco = barcos[barco_posicion[NUMERO_BARCO]]
		orientacion_barco_perpendicular = FILA
		orientacion_barco = COLUMNA
		demanda_orientacion = demanda_columna_incumplida
		demanda_orientacion_perpendicular = demanda_fila_incumplida
		if diferencia_columna > 0:
			orientacion_barco_perpendicular = COLUMNA
			orientacion_barco = FILA
			demanda_orientacion = demanda_fila_incumplida
			demanda_orientacion_perpendicular = demanda_columna_incumplida
		demanda_orientacion[pos_extremo_inicial[orientacion_barco]] -= largo_barco
		for avance in range(min(pos_extremo_inicial[orientacion_barco_perpendicular], pos_extremo_final[orientacion_barco_perpendicular]), max(pos_extremo_inicial[orientacion_barco_perpendicular], pos_extremo_final[orientacion_barco_perpendicular]) + 1):
			demanda_orientacion_perpendicular[avance] -= 1
			posicion_ocupada = (pos_extremo_inicial[FILA], avance)
			if diferencia_fila > 0:
				posicion_ocupada = (avance, pos_extremo_inicial[COLUMNA])
			casilleros_ocupados[posicion_ocupada] = True
	for demanda in demanda_fila_incumplida:
		if demanda != 0:
		    return False
	for demanda in demanda_columna_incumplida:
		if demanda != 0:
		    return False
	return True



def estan_todos_los_casilleros_disponibles(pos_extremo_inicial, pos_extremo_final, casilleros_ocupados):
	direccion = obtener_direccion(pos_extremo_inicial, pos_extremo_final)
	if direccion == (0,0):
		return not (pos_extremo_inicial in casilleros_ocupados)

	disposicion_avance = FILA
	if direccion[COLUMNA] > 0:
		disposicion_avance = COLUMNA

	pos_avance_inicial = pos_extremo_inicial[disposicion_avance]
	pos_avance_final = pos_extremo_final[disposicion_avance]
	direccion_avance = direccion[disposicion_avance]
	for avance in range(pos_avance_inicial, pos_avance_final + direccion_avance, direccion_avance):
		if disposicion_avance == FILA and (avance, pos_extremo_inicial[COLUMNA]) in casilleros_ocupados:
			return False
		elif disposicion_avance == COLUMNA and (pos_extremo_inicial[FILA], avance) in casilleros_ocupados:
			return False
	return True


def obtener_direccion(pos_extremo_inicial, pos_extremo_final):
	diferencia_fila = pos_extremo_final[FILA] - pos_extremo_inicial[FILA]
	diferencia_columna = pos_extremo_final[COLUMNA] - pos_extremo_inicial[COLUMNA]
	if diferencia_fila == 0 and diferencia_columna == 0:
		return (0, 0)
	elif diferencia_fila == 0:
		return (0, int(diferencia_columna/abs(diferencia_columna)))
	else:
		return (int(diferencia_fila/abs(diferencia_fila)), 0)



def barco_posicionado_a_lo_largo_de_la_columna(barco_posicion):
	pos_extremo_inicial = barco_posicion[POSICION_EXTREMO_INICIAL]
	pos_extremo_final = barco_posicion[POSICION_EXTREMO_FINAL]