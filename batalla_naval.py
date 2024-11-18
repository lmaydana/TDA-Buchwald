import numpy as np
from itertools import product


def calcular_demanda_cumplida(tablero, demandas_filas, demandas_columnas):
    """
    Calcula la cantidad de demanda cumplida en filas y columnas.
    """
    elementos_no_cero_filas = (tablero != 0).sum(axis=1)
    elementos_no_cero_columnas = (tablero != 0).sum(axis=0)

    cumplida_filas = np.minimum(demandas_filas, elementos_no_cero_filas).sum()
    cumplida_columnas = np.minimum(demandas_columnas, elementos_no_cero_columnas).sum()

    return cumplida_filas + cumplida_columnas



def puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
    """
    Verifica si es posible colocar un barco respetando:
    - Restricciones de adyacencia.
    - Que no exceda las demandas de filas y columnas.
    """
    filas, columnas = tablero.shape

    if orientacion == 'H':  # Horizontal.
        if columna + barco > columnas:
            return False
        if any(tablero[fila, columna:columna + barco] != 0):
            return False
        if demandas_filas[fila] - (tablero[fila] != 0).sum() < barco:
            return False
        for j in range(columna, columna + barco):
            if demandas_columnas[j] - (tablero[:, j] != 0).sum() < 1:
                return False
        for i in range(max(0, fila - 1), min(filas, fila + 2)):
            for j in range(max(0, columna - 1), min(columnas, columna + barco + 1)):
                if tablero[i, j] != 0 and (i != fila or j < columna or j >= columna + barco):
                    return False

    elif orientacion == 'V':  # Vertical.
        if fila + barco > filas:
            return False
        if any(tablero[fila:fila + barco, columna] != 0):
            return False
        if demandas_columnas[columna] - (tablero[:, columna] != 0).sum() < barco:
            return False
        for i in range(fila, fila + barco):
            if demandas_filas[i] - (tablero[i] != 0).sum() < 1:
                return False
        for i in range(max(0, fila - 1), min(filas, fila + barco + 1)):
            for j in range(max(0, columna - 1), min(columnas, columna + 2)):
                if tablero[i, j] != 0 and (j != columna or i < fila or i >= fila + barco):
                    return False

    return True


def colocar_barco(tablero, barco, fila, columna, orientacion, id_barco):
    """
    Coloca o retira un barco en el tablero y actualiza las demandas.
    """
    for i in range(barco):
        if orientacion == 'H':
            tablero[fila][columna + i] = id_barco if id_barco != 0 else 0

        elif orientacion == 'V':
            tablero[fila + i][columna] = id_barco if id_barco != 0 else 0



def obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas, tablero):
    """
    Obtiene listas de filas y columnas priorizadas por demanda restante absoluta (mayor urgencia).
    """
    # Demanda restante en filas y columnas.
    demanda_restante_filas, demanda_restante_columnas = calcular_demandas_restantes(tablero, demandas_filas, demandas_columnas)

    # Priorizar por la demanda restante absoluta (filas/columnas con mayor demanda restante primero).
    filas_prioritarias = np.argsort(-demanda_restante_filas).tolist()
    columnas_prioritarias = np.argsort(-demanda_restante_columnas).tolist()

    print(f"Filas prioritarias: {filas_prioritarias}")
    print(f"Columnas prioritarias: {columnas_prioritarias}")

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
                demandas_restantes_filas[fila] = max(0, demandas_restantes_filas[fila] - 1)
                demandas_restantes_columnas[columna] = max(0, demandas_restantes_columnas[columna] - 1)

    return demandas_restantes_filas, demandas_restantes_columnas


def evaluar_posicion(tablero, barco, fila, columna, orientacion, demandas_restantes_filas, demandas_restantes_columnas):
    """
    Evalua la cantidad de demanda cumplida al colocar un barco en la posicion y orientacion dadas.
    """
    demanda_cumplida = 0
    for i in range(barco):
        if orientacion == 'H' and columna + i < len(tablero[0]):
            demanda_cumplida += demandas_restantes_filas[fila] + demandas_restantes_columnas[columna + i]
        elif orientacion == 'V' and fila + i < len(tablero):
            demanda_cumplida += demandas_restantes_filas[fila + i] + demandas_restantes_columnas[columna]
    return demanda_cumplida


def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
    # Ordenar los barcos de mayor a menor longitud.
    barcos = sorted(barcos, reverse=True)
    demanda_cumplida_inicial = 0
    return batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_cumplida_inicial, 0, 0)


def batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_cumplida, indice, mejor_cumplida):
    # Caso base: todos los barcos han sido procesados.
    if indice >= len(barcos):
        demanda_total = demandas_filas.sum() + demandas_columnas.sum()
        demanda_incumplida = demanda_total - demanda_cumplida
        if demanda_cumplida > mejor_cumplida:
            mejor_cumplida = demanda_cumplida
            print(f"Nueva mejor solución encontrada:")
            print(tablero)
            print(f"Demanda cumplida: {demanda_cumplida}, Demanda incumplida: {demanda_incumplida}")
        return mejor_cumplida, tablero.copy()

    
    barco = barcos[indice]
    id_barco = indice + 1  # Identificador unico para el barco.
    mejor_tablero = None  # Tablero asociado a la mejor solucion.

    # Obtener filas y columnas priorizadas.
    filas_prioritarias, columnas_prioritarias = obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas, tablero.copy())

    # Probar todas las combinaciones de posicion y orientacion.
    for fila in filas_prioritarias:
        for columna in columnas_prioritarias:
            for orientacion in ['V', 'H']:
                if puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
                    # Colocar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, id_barco)
                    nueva_cumplida = calcular_demanda_cumplida(tablero, demandas_filas, demandas_columnas)

                    # Poda.
                    if nueva_cumplida > mejor_cumplida:
                        resultado_cumplida, resultado_tablero = batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, nueva_cumplida, indice + 1, mejor_cumplida)
                        if resultado_cumplida > mejor_cumplida:
                            mejor_cumplida = resultado_cumplida
                            mejor_tablero = resultado_tablero.copy()

                    # Retirar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, 0)

    # Omitir barco actual.
    resultado_cumplida, resultado_tablero = batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_cumplida, indice + 1, mejor_cumplida)
    if resultado_cumplida > mejor_cumplida:
        mejor_cumplida = resultado_cumplida
        mejor_tablero = resultado_tablero

    return mejor_cumplida, mejor_tablero
