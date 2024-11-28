import pulp

def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
	problema = pulp.LpProblem("batalla_naval", pulp.LpMaximize)
	variables_barcos = []
	variables_barcos_posiciones = []
	variables_celdas = []
	for fila in tablero:
		fila_variables = []
		for celda in fila:
			fila_variables.append(pulp.LpVariable("C(" + str(len(variables_celdas)) + "," + str(len(fila_variables)) + ")", cat="Binary"))
		variables_celdas.append(fila_variables)

	for indice_barco in range(len(barcos)):
		variables_barcos.append(pulp.LpVariable("B"+str(indice_barco), cat = "Binary"))

	for indice_barco in range(len(barcos)):
		barco_pos = []
		for pos in range(len(tablero)*len(tablero[0])):
			barco_pos.append(pulp.LpVariable("B" + str(indice_barco) + "P" + str(pos), cat="Binary"))
		variables_barcos_posiciones.append(barco_pos)

	for pos in range(len(tablero)*len(tablero[0])):
		problema += pulp.LpAffineExpression([(variables_barcos_posiciones[indice_barco][pos], 1) for indice_barco in range(len(barcos))]) <= 1

	for indice_barco in range(len(barcos)):
		problema += pulp.LpAffineExpression([(variables_barcos_posiciones[indice_barco][pos],1) for pos in range(len(tablero)*len(tablero[0]))]) <= barcos[indice_barco]*variables_barcos[indice_barco]
	
	for indice_barco in range(len(barcos)):
		variables_and_filas = []
		variables_and_columnas = []
		or_columnas = pulp.LpVariable("SE_PONE_EN_FILA_BARCO_"+str(indice_barco), cat = "Binary")
		for fila in range(len(tablero)):
			for comienzo in range(len(tablero[0]) - barcos[indice_barco]):
				variable_and = pulp.LpVariable("AND_COLUMNAS_ACTIVAS_DESDE_"+str(comienzo)+"_HASTA_"+str(comienzo+barcos[indice_barco]) + "_FILA_"+str(fila)+"BARCO_"+str(indice_barco), cat = "Binary")
				variable_and_borde_vacio = pulp.LpVariable("AND_BORDE_LIBRE_COLUMNAS_ACTIVAS_DESDE_"+str(comienzo)+"_HASTA_"+str(comienzo+barcos[indice_barco]) + "_FILA_"+str(fila)+"BARCO_"+str(indice_barco), cat = "Binary")
				for filab in range(max(fila - 1,0), min(fila + 2, len(tablero))):
					for columnab in range(max(0,comienzo - 1), min(len(tablero[0]),comienzo + barcos[indice_barco] + 1)):
						for indice_otro_barco in range(0, indice_barco):
							problema += variable_and_borde_vacio <= 1 - variables_barcos_posiciones[indice_otro_barco][len(tablero[0])*filab + columnab]
						for indice_otro_barco in range(indice_barco + 1, len(barcos)):
							problema += variable_and_borde_vacio <= 1 - variables_barcos_posiciones[indice_otro_barco][len(tablero[0])*filab + columnab]
				problema += variable_and*barcos[indice_barco] <= pulp.LpAffineExpression([(variables_barcos_posiciones[indice_barco][len(tablero[0])*fila + columna],1) for columna in range(comienzo, comienzo + barcos[indice_barco])])
				problema += variable_and <= variable_and_borde_vacio
				variables_and_filas.append(variable_and)
		problema += pulp.LpAffineExpression([(var_and_fila, 1) for var_and_fila in variables_and_filas]) <= 1
		problema += or_columnas <= pulp.LpAffineExpression([(var_and_fila, 1) for var_and_fila in variables_and_filas])
		or_filas = pulp.LpVariable("SE_PONE_EN_COLUMNA_BARCO_"+str(indice_barco), cat = "Binary")
		for columna in range(len(tablero[0])):
			for comienzo in range(len(tablero) - barcos[indice_barco]):
				variable_and = pulp.LpVariable("AND_FILAS_ACTIVAS_DESDE_"+str(comienzo)+"_HASTA_"+str(comienzo+barcos[indice_barco])+"_COLUMNA_"+str(columna)+"BARCO_"+str(indice_barco), cat = "Binary")
				variable_and_borde_vacio = pulp.LpVariable("AND_BORDE_LIBRE_FILAS_ACTIVAS_DESDE_"+str(comienzo)+"_HASTA_"+str(comienzo+barcos[indice_barco]) + "_COLUMNA_"+str(columna)+"BARCO_"+str(indice_barco), cat = "Binary")
				for columnab in range(max(columna - 1,0), min(columna + 2, len(tablero[0]))):
					for filab in range(max(0, comienzo - 1),min(len(tablero) ,comienzo + barcos[indice_barco] + 1)):
						for indice_otro_barco in range(0, indice_barco):
							problema += variable_and_borde_vacio <= 1 - variables_barcos_posiciones[indice_otro_barco][len(tablero[0])*filab + columnab]
						for indice_otro_barco in range(indice_barco + 1, len(barcos)):
							problema += variable_and_borde_vacio <= 1 - variables_barcos_posiciones[indice_otro_barco][len(tablero[0])*filab + columnab]
				problema += variable_and*barcos[indice_barco] <= pulp.LpAffineExpression([(variables_barcos_posiciones[indice_barco][len(tablero[0])*fila + columna],1) for fila in range(comienzo, comienzo + barcos[indice_barco])])
				problema += variable_and <= variable_and_borde_vacio
				variables_and_columnas.append(variable_and)
		problema += pulp.LpAffineExpression([(var_and_columna, 1) for var_and_columna in variables_and_columnas]) <= 1
		problema += or_filas <= pulp.LpAffineExpression([(var_and_columna, 1) for var_and_columna in variables_and_columnas])
		problema += or_filas + or_columnas <= 1
		problema += variables_barcos[indice_barco] <= or_filas + or_columnas

	for fila in range(len(tablero)):
		problema += pulp.LpAffineExpression([(variables_barcos_posiciones[indice_barco][len(tablero[0])*fila + columna], 1) for indice_barco in range(len(barcos)) for columna in range(len(tablero[0]))]) <= demandas_filas[fila]

	for columna in range(len(tablero[0])):
		problema += pulp.LpAffineExpression([(variables_barcos_posiciones[indice_barco][len(tablero[0])*fila + columna], 1) for indice_barco in range(len(barcos)) for fila in range(len(tablero))]) <= demandas_columnas[columna]
	for fila in range(len(tablero)):
		for columna in range(len(tablero[0])):
			problema += variables_celdas[fila][columna] <= pulp.LpAffineExpression([(variables_barcos_posiciones[pos_barco][len(tablero[0])*fila + columna], 1) for pos_barco in range(len(barcos))])
	problema += pulp.LpAffineExpression([(celda,2) for fila in variables_celdas for celda in fila])
	problema.solve()
	
	for fila in range(len(tablero)):
		for columna in range(len(tablero[fila])):
			tablero[fila][columna] = sum([pulp.value(variables_barcos_posiciones[indice_barco][len(tablero[0])*fila + columna])*(indice_barco + 1) for indice_barco in range(len(barcos))])
	
	return pulp.value(problema.objective),tablero
