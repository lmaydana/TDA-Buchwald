import numpy as np
from itertools import product


def calcular_demanda_incumplida(tablero, demandas_filas, demandas_columnas):
    """
    Calcula la demanda incumplida en filas y columnas.
    Retorna la suma total de demandas incumplidas.
    """

    # Contar el numero de elementos diferentes de 0 en cada fila.
    elementos_no_cero_filas = (tablero != 0).sum(axis=1)
    # Contar el numero de elementos diferentes de 0 en cada columna.
    elementos_no_cero_columnas = (tablero != 0).sum(axis=0)

    diferencia_filas = np.maximum(demandas_filas - elementos_no_cero_filas, 0)
    diferencia_columnas = np.maximum(demandas_columnas - elementos_no_cero_columnas, 0)
    return diferencia_filas.sum() + diferencia_columnas.sum()


def puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
    """
    Verifica si es posible colocar un barco de forma indivisible.
    """
    filas, columnas = tablero.shape # Para obtener dimensiones del tablero. -> (#filas, #columnas)
    if orientacion == 'H':  # Horizontal.
        if columna + barco > columnas or any(tablero[fila, columna:columna + barco] != 0):  # Se sale del tablero o hay conflicto.
            return False
        # Verificar restricciones de demanda.
        if tablero[fila, columna:columna + barco].sum() + barco > demandas_filas[fila]:
            return False
        if any(tablero[:, columna:columna + barco].sum(axis=0) + 1 > demandas_columnas[columna:columna + barco]):
            return False
    elif orientacion == 'V':  # Vertical.
        if fila + barco > filas or any(tablero[fila:fila + barco, columna] != 0):  # Se sale del tablero o hay conflicto.
            return False
        # Verificar restricciones de demanda.
        if tablero[fila:fila + barco, columna].sum() + barco > demandas_columnas[columna]:
            return False
        if any(tablero[fila:fila + barco, :].sum(axis=1) + 1 > demandas_filas[fila:fila + barco]):
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
    demanda_incumplida = calcular_demanda_incumplida(tablero, demandas_filas, demandas_columnas)

    return batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_incumplida)

def batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_incumplida, indice=0):
    """
    Algoritmo de backtracking que mantiene los barcos como entidades indivisibles.
    """
    if indice == len(barcos):
        # Todos los barcos han sido procesados.
        return demanda_incumplida, tablero.copy()
    
    barco = barcos[indice]
    mejor_demanda = demanda_incumplida
    mejor_tablero = tablero.copy()
    id_barco = indice + 1  # Identificador unico para el barco.
    
    for fila, columna in product(range(tablero.shape[0]), range(tablero.shape[1])):
        for orientacion in ['H', 'V']:
            if puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
                # Colocar el barco.
                colocar_barco(tablero, barco, fila, columna, orientacion, id_barco)
                nueva_demanda_incumplida = calcular_demanda_incumplida(tablero, demandas_filas, demandas_columnas)
                if nueva_demanda_incumplida < mejor_demanda:
                    resultado_demanda, resultado_tablero = batalla_naval_bt(
                        tablero, barcos, demandas_filas, demandas_columnas, nueva_demanda_incumplida, indice + 1
                    )
                    if resultado_demanda < mejor_demanda:
                        mejor_demanda, mejor_tablero = resultado_demanda, resultado_tablero
                # Retirar el barco.
                colocar_barco(tablero, barco, fila, columna, orientacion, 0)
    
    # Omitir el barco actual.
    resultado_demanda, resultado_tablero = batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, demanda_incumplida, indice + 1)
    if resultado_demanda < mejor_demanda:
        mejor_demanda, mejor_tablero = resultado_demanda, resultado_tablero

    return mejor_demanda, mejor_tablero
