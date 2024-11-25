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
    Verifica si es posible colocar un barco en cualquier dirección (derecha/izquierda o abajo/arriba)
    respetando las restricciones de:
    - Adyacencia.
    - Demandas de filas y columnas.
    """
    tablero_cop = tablero.copy()
    demandas_filas_cop = demandas_filas.copy()
    demandas_columnas_cop = demandas_columnas.copy()
    filas, columnas = tablero.shape

    if orientacion == 'H':  # Horizontal
        # Verificar hacia la derecha
        if columna + barco <= columnas:
            if all(tablero_cop[fila, columna:columna + barco] == 0) and \
                    demandas_filas_cop[fila] - (tablero_cop[fila] != 0).sum() >= barco and \
                    all(demandas_columnas_cop[j] - (tablero_cop[:, j] != 0).sum() >= 1 for j in range(columna, columna + barco)):
                # Verificar adyacencia
                if all(tablero_cop[max(0, fila - 1):min(filas, fila + 2), max(0, columna - 1):min(columnas, columna + barco + 1)].flatten() == 0):
                    return True


    elif orientacion == 'V':  # Vertical
        # Verificar hacia abajo
        if fila + barco <= filas:
            if all(tablero_cop[fila:fila + barco, columna] == 0) and \
                    demandas_columnas_cop[columna] - (tablero_cop[:, columna] != 0).sum() >= barco and \
                    all(demandas_filas_cop[i] - (tablero_cop[i] != 0).sum() >= 1 for i in range(fila, fila + barco)):
                # Verificar adyacencia
                if all(tablero_cop[max(0, fila - 1):min(filas, fila + barco + 1), max(0, columna - 1):min(columnas, columna + 2)].flatten() == 0):
                    return True


    return False


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


def obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas, tablero):
    """
    Obtiene listas de filas y columnas priorizadas por demanda restante absoluta (mayor urgencia).
    """
    # Demanda restante en filas y columnas.
    demanda_restante_filas, demanda_restante_columnas = calcular_demandas_restantes(tablero, demandas_filas, demandas_columnas)

    # Priorizar por la demanda restante absoluta.
    filas_prioritarias = np.argsort(-demanda_restante_filas).tolist() # Devuelve los indices.
    columnas_prioritarias = np.argsort(-demanda_restante_columnas).tolist()

    print(f"Filas prioritarias: {filas_prioritarias}")
    print(f"Columnas prioritarias: {columnas_prioritarias}")

    return demanda_restante_filas, demanda_restante_columnas, filas_prioritarias, columnas_prioritarias


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
    demanda_cumplida_inicial = 0
    sol_optima = [0, tablero.copy()]
    sol_parcial = [0, tablero]
    batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, 0, sol_parcial, sol_optima)
    return sol_optima


def batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, indice, sol_parcial, sol_optima):
    
    if indice >= len(barcos):
        if sol_parcial[0] > sol_optima[0]:
            sol_optima[0] = sol_parcial[0]
            sol_optima[1] = sol_parcial[1].copy()
        return

    if sol_parcial[0] > sol_optima[0]:
        sol_optima[0] = sol_parcial[0]
        sol_optima[1] = sol_parcial[1].copy()

    if sol_parcial[0] + (sum(barcos[indice:])*2) <= sol_optima[0]:
        return

    barco = barcos[indice]
    id_barco = indice + 1  # Identificador unico para el barco.

    # Obtener filas y columnas priorizadas.
    demanda_restante_filas, demanda_restante_columnas, filas_prioritarias, columnas_prioritarias = obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas, tablero.copy())

    #cota_superior = 0

    #for barco_res in barcos[indice:]:
    cota_superior = sum(max(0, d - barco) for d in demanda_restante_filas) + sum(max(0, d - barco) for d in demanda_restante_columnas)
    """Esto seria lo que mas podria abarcar el barco, dejando la sumatoria de demandas restastenes en fila y columna"""
    if cota_superior >= (demandas_filas.sum() + demandas_columnas.sum() - sol_optima[0]):
        return

    # Probar todas las combinaciones de posicion y orientacion.
    for fila in filas_prioritarias:
        if demandas_filas[fila] == 0: continue
        for columna in columnas_prioritarias:
            if demandas_columnas[columna] == 0: continue
            for orientacion in ['H', 'V']:
                if puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
                    # Colocar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, id_barco)

                    sol_parcial[0] = calcular_demanda_cumplida(tablero, demandas_filas, demandas_columnas)
                    sol_parcial[1] = tablero.copy()
                    if sol_parcial[0] > sol_optima[0] or sol_parcial[0] + (sum(barcos[indice:])) >= sol_optima[0]:    
                        batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, indice + 1, sol_parcial, sol_optima)
                    # Retirar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, 0)

    return batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, indice + 1, sol_parcial, sol_optima)
