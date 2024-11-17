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



def puede_colocar_barco(tablero, barco, fila, columna, orientacion):
    """
    Verifica si es posible colocar un barco de forma indivisible, respetando las restricciones de adyacencia.
    """
    filas, columnas = tablero.shape

    if orientacion == 'H':  # Horizontal.
        if columna + barco > columnas:  # El barco se sale del tablero.
            return False
        # Verificar si el espacio esta ocupado.
        if any(tablero[fila, columna:columna + barco] != 0):
            return False
        # Verificar adyacencia
        for i in range(max(0, fila - 1), min(filas, fila + 2)):  # Filas vecinas.
            for j in range(max(0, columna - 1), min(columnas, columna + barco + 1)):  # Columnas vecinas.
                if tablero[i, j] != 0 and (i != fila or j < columna or j >= columna + barco):
                    return False

    elif orientacion == 'V':  # Vertical.
        if fila + barco > filas:  # El barco se sale del tablero.
            return False
        # Verificar si el espacio esta ocupado.
        if any(tablero[fila:fila + barco, columna] != 0):
            return False
        # Verificar adyacencia.
        for i in range(max(0, fila - 1), min(filas, fila + barco + 1)):  # Filas vecinas.
            for j in range(max(0, columna - 1), min(columnas, columna + 2)):  # Columnas vecinas.
                if tablero[i, j] != 0 and (j != columna or i < fila or i >= fila + barco):
                    return False

    return True


def colocar_barco(tablero, barco, fila, columna, orientacion, id_barco):
    """
    Coloca un barco indivisible en el tablero con un identificador unico.
    """
    if orientacion == 'H':
        tablero[fila, columna:columna + barco] = id_barco
    elif orientacion == 'V':
        tablero[fila:fila + barco, columna] = id_barco


def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
    # Ordenar los barcos de mayor a menor longitud.
    barcos = sorted(barcos, reverse=True)
    demanda_cumplida_inicial = calcular_demanda_cumplida(tablero, demandas_filas, demandas_columnas)
    return batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_cumplida_inicial)


def batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_cumplida, indice=0, mejor_cumplida=0):
    # Caso base: todos los barcos han sido procesados.
    if indice == len(barcos):
        demanda_total = demandas_filas.sum() + demandas_columnas.sum()
        demanda_incumplida = demanda_total - demanda_cumplida
        if demanda_cumplida > mejor_cumplida:
            mejor_cumplida = demanda_cumplida
            print(f"Nueva mejor solución encontrada:")
            print(tablero)
            print(f"Demanda cumplida: {demanda_cumplida}, Demanda incumplida: {demanda_incumplida}")
        return demanda_cumplida, tablero.copy()

    barco = barcos[indice]
    id_barco = indice + 1  # Identificador unico para el barco.
    mejor_tablero = None  # Tablero asociado a la mejor solucion.

    # Probar todas las combinaciones de posicion y orientacion para el barco actual.
    for fila, columna in product(range(tablero.shape[0]), range(tablero.shape[1])):
        for orientacion in ['H', 'V']:
            if puede_colocar_barco(tablero, barco, fila, columna, orientacion):
                # Colocar el barco.
                colocar_barco(tablero, barco, fila, columna, orientacion, id_barco)
                nueva_cumplida = calcular_demanda_cumplida(tablero, demandas_filas, demandas_columnas)

                # Poda: si la nueva configuracion no mejora, no seguir explorando.
                if nueva_cumplida > mejor_cumplida:
                    resultado_cumplida, resultado_tablero = batalla_naval_bt(
                        tablero, barcos, demandas_filas, demandas_columnas, nueva_cumplida, indice + 1, mejor_cumplida
                    )
                    if resultado_cumplida > mejor_cumplida:
                        mejor_cumplida = resultado_cumplida
                        mejor_tablero = resultado_tablero
                # Retirar el barco.
                colocar_barco(tablero, barco, fila, columna, orientacion, 0)

    # Omitir el barco actual y probar otras configuraciones.
    resultado_cumplida, resultado_tablero = batalla_naval_bt(
        tablero, barcos, demandas_filas, demandas_columnas, demanda_cumplida, indice + 1, mejor_cumplida
    )
    if resultado_cumplida > mejor_cumplida:
        mejor_cumplida = resultado_cumplida
        mejor_tablero = resultado_tablero

    return mejor_cumplida, mejor_tablero
