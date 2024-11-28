import numpy as np
from itertools import product


def actualizar_demandas(tablero, barco, orientacion, fila, columna, demandas_filas, demandas_columnas, signo):
    """
    Calcula la cantidad de demanda cumplida en filas y columnas.
    """
    if orientacion == 'H':
        demandas_filas[fila] += signo*barco
        for pos_columna in range(columna, min(columna + barco, len(tablero[0]))):
            demandas_columnas[pos_columna] += signo*1
    else:
        demandas_columnas[columna] += signo*barco
        for pos_fila in range(fila, min(fila + barco, len(tablero))):
            demandas_filas[pos_fila] += signo*1



def puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
    """
    Verifica si es posible colocar un barco en cualquier dirección (derecha/izquierda o abajo/arriba)
    respetando las restricciones de:
    - Adyacencia.
    - Demandas de filas y columnas.
    """
    if orientacion == 'H':
        if columna + barco > len(tablero[0]):
            return False
        for pos_columna in range(columna, columna + barco):
            if demandas_columnas[pos_columna] == 0:
                return False
        return demandas_filas[fila] >= barco and el_sector_esta_vacio(tablero, barco, fila, columna, orientacion)
    else:
        if fila + barco > len(tablero):
            return False
        for pos_fila in range(fila, fila + barco):
            if demandas_filas[pos_fila] == 0:
                return False
        return demandas_columnas[columna] >= barco and el_sector_esta_vacio(tablero, barco, fila, columna, orientacion)


def el_sector_esta_vacio(tablero, barco, fila, columna, orientacion):
    if orientacion == 'H':
        for pos_fila in range(max(fila - 1, 0), min(fila + 2, len(tablero))):
            for pos_columna in range(max(columna - 1, 0), min(columna + barco + 1, len(tablero[0]))):
                if tablero[pos_fila][pos_columna] != 0:
                    return False
    else:
        for pos_fila in range(max(fila - 1, 0), min(fila + barco + 1, len(tablero))):
            for pos_columna in range(max(columna - 1, 0), min(columna + 2, len(tablero[0]))):
                if tablero[pos_fila][pos_columna] != 0:
                    return False
    return True



def colocar_barco(tablero, barco, fila, columna, orientacion, id_barco):
    """
    Coloca o retira un barco en el tablero, eligiendo la direccion.
    - Si es horizontal ('H'), elige extenderse a la derecha.
    - Si es vertical ('V'), elige extenderse hacia abajo.
    """
    if orientacion == 'H':
        for i in range(barco):
            tablero[fila][columna + i] = id_barco 
    elif orientacion == 'V':
        for i in range(barco):
            tablero[fila + i][columna] = id_barco 


def obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas):
    """
    Obtiene listas de filas y columnas priorizadas por demanda restante absoluta (mayor urgencia).
    """
    # Demanda restante en filas y columnas.
    #demanda_restante_filas, demanda_restante_columnas = calcular_demandas_restantes(tablero, demandas_filas, demandas_columnas)

    # Priorizar por la demanda restante absoluta.
    filas_prioritarias = np.argsort(-demandas_filas).tolist() # Devuelve los indices.
    columnas_prioritarias = np.argsort(-demandas_columnas).tolist()

    #print(f"Filas prioritarias: {filas_prioritarias}")
    #print(f"Columnas prioritarias: {columnas_prioritarias}")

    return filas_prioritarias, columnas_prioritarias


def calcular_demandas_restantes(tablero, demandas_filas, demandas_columnas):
    """
    Calcula cuanta demanda falta por cubrir en cada fila y columna.
    """
    demandas_restantes_filas = demandas_filas.copy()
    demandas_restantes_columnas = demandas_columnas.copy()
    
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            if tablero[fila][columna] != 0:  # Hay un barco en esta celda.
                demandas_restantes_filas[fila] = demandas_restantes_filas[fila] - 1
                demandas_restantes_columnas[columna] = demandas_restantes_columnas[columna] - 1

    return demandas_restantes_filas, demandas_restantes_columnas


def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
    # Ordenar los barcos de mayor a menor longitud.
    barcos = sorted(barcos, reverse=True)
    demanda_inicial = sum(demandas_filas) + sum(demandas_columnas)
    demandas_filas_cop = demandas_filas.copy()
    demandas_columnas_cop = demandas_columnas.copy()
    solucion_tablero = tablero.copy()
    solucion_demandas_filas = demandas_filas_cop.copy()
    solucion_demandas_columnas = demandas_columnas_cop.copy()
    batalla_naval_bt(tablero.copy(), barcos, demandas_filas_cop, demandas_columnas_cop, demanda_inicial, 0, solucion_tablero, solucion_demandas_filas, solucion_demandas_columnas)
    return demanda_inicial - sum(solucion_demandas_filas) - sum(solucion_demandas_columnas), solucion_tablero

def maxima_cantidad_contiguos_fila_columna(demandas_filas, demandas_columnas):
    maximos_contiguos_filas = 0
    contiguos_actual = 0
    for demanda_fila in demandas_filas:
        if demanda_fila > 0:
            contiguos_actual += 1
        else:
            if contiguos_actual > maximos_contiguos_filas:
                maximos_contiguos_filas = contiguos_actual
            contiguos_actual = 0

    maximos_contiguos_columnas = 0
    contiguos_actual = 0
    for demanda_columna in demandas_columnas:
        if demanda_columna > 0:
            contiguos_actual += 1
        else:
            if contiguos_actual > maximos_contiguos_columnas:
                maximos_contiguos_columnas = contiguos_actual
            contiguos_actual = 0
    return maximos_contiguos_filas, maximos_contiguos_columnas

    
def batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_inicial, indice, mejor_tablero, mejor_demanda_sobrante_fila, mejor_demanda_sobrante_columna):
    suma_demandas_filas =  sum(demandas_filas)
    suma_demandas_columnas = sum(demandas_columnas)
    demanda_sobrante_actual = suma_demandas_filas + suma_demandas_columnas
    mejor_demanda_sobrante = sum(mejor_demanda_sobrante_fila) + sum(mejor_demanda_sobrante_columna)
    if indice >= len(barcos):
        if demanda_sobrante_actual < mejor_demanda_sobrante:
            np.copyto(mejor_tablero, tablero)
            np.copyto(mejor_demanda_sobrante_fila, demandas_filas)
            np.copyto(mejor_demanda_sobrante_columna, demandas_columnas)

        return False

    if demanda_sobrante_actual < mejor_demanda_sobrante:
            np.copyto(mejor_tablero, tablero)
            np.copyto(mejor_demanda_sobrante_fila, demandas_filas)
            np.copyto(mejor_demanda_sobrante_columna, demandas_columnas)
            mejor_demanda_sobrante = sum(mejor_demanda_sobrante_fila) + sum(mejor_demanda_sobrante_columna)

    mejor_demanda_cumplida = demanda_inicial - mejor_demanda_sobrante
    demanda_cumplida = demanda_inicial - demanda_sobrante_actual

    if demanda_cumplida == demanda_inicial:
        np.copyto(mejor_tablero, tablero)
        np.copyto(mejor_demanda_sobrante_fila, demandas_filas)
        np.copyto(mejor_demanda_sobrante_columna, demandas_columnas)
        return True

    if demanda_cumplida + 2*sum(barcos[indice:]) < mejor_demanda_cumplida or max(max(demandas_filas), max(demandas_columnas)) < barcos[-1]:
        return False

    barco = barcos[indice]
    id_barco = indice + 1  # Identificador unico para el barco.

    if barco > max(demandas_filas) and barco > max(demandas_columnas):
        return batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_inicial, indice + 1, mejor_tablero, mejor_demanda_sobrante_fila, mejor_demanda_sobrante_columna)

    # Obtener filas y columnas priorizadas.
    filas_prioritarias, columnas_prioritarias = obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas)

    # Probar todas las combinaciones de posicion y orientacion.
    for fila in filas_prioritarias:
        if demandas_filas[fila] == 0: continue
        for columna in columnas_prioritarias:
            if demandas_columnas[columna] == 0: continue
            for orientacion in ['H', 'V']:
                if puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
                    # Colocar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, id_barco)
                    actualizar_demandas(tablero, barco, orientacion, fila, columna, demandas_filas, demandas_columnas, -1)
                    demanda_sobrante_actual -= 2*barco
                    respuesta = batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_inicial, indice + 1, mejor_tablero, mejor_demanda_sobrante_fila, mejor_demanda_sobrante_columna)
                    if respuesta:
                        return respuesta
                    # Retirar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, 0)
                    actualizar_demandas(tablero, barco, orientacion, fila, columna, demandas_filas, demandas_columnas, 1)
                    demanda_sobrante_actual += 2*barco

    return batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_inicial, indice + 1, mejor_tablero, mejor_demanda_sobrante_fila, mejor_demanda_sobrante_columna)