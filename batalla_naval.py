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
    filas, columnas = tablero.shape

    if orientacion == 'H':  # Horizontal
        # Verificar hacia la derecha
        if columna + barco <= columnas:
            if all(tablero[fila, columna:columna + barco] == 0) and \
                    demandas_filas[fila] - (tablero[fila] != 0).sum() >= barco and \
                    all(demandas_columnas[j] - (tablero[:, j] != 0).sum() >= 1 for j in range(columna, columna + barco)):
                # Verificar adyacencia
                if all(tablero[max(0, fila - 1):min(filas, fila + 2), max(0, columna - 1):min(columnas, columna + barco + 1)].flatten() == 0):
                    return True

        # Verificar hacia la izquierda
        if columna - barco + 1 >= 0:
            if all(tablero[fila, columna - barco + 1:columna + 1] == 0) and \
                    demandas_filas[fila] - (tablero[fila] != 0).sum() >= barco and \
                    all(demandas_columnas[j] - (tablero[:, j] != 0).sum() >= 1 for j in range(columna - barco + 1, columna + 1)):
                # Verificar adyacencia
                if all(tablero[max(0, fila - 1):min(filas, fila + 2), max(0, columna - barco):min(columnas, columna + 2)].flatten() == 0):
                    return True

    elif orientacion == 'V':  # Vertical
        # Verificar hacia abajo
        if fila + barco <= filas:
            if all(tablero[fila:fila + barco, columna] == 0) and \
                    demandas_columnas[columna] - (tablero[:, columna] != 0).sum() >= barco and \
                    all(demandas_filas[i] - (tablero[i] != 0).sum() >= 1 for i in range(fila, fila + barco)):
                # Verificar adyacencia
                if all(tablero[max(0, fila - 1):min(filas, fila + barco + 1), max(0, columna - 1):min(columnas, columna + 2)].flatten() == 0):
                    return True

        # Verificar hacia arriba
        if fila - barco + 1 >= 0:
            if all(tablero[fila - barco + 1:fila + 1, columna] == 0) and \
                    demandas_columnas[columna] - (tablero[:, columna] != 0).sum() >= barco and \
                    all(demandas_filas[i] - (tablero[i] != 0).sum() >= 1 for i in range(fila - barco + 1, fila + 1)):
                # Verificar adyacencia
                if all(tablero[max(0, fila - barco):min(filas, fila + 2), max(0, columna - 1):min(columnas, columna + 2)].flatten() == 0):
                    return True

    return False


def colocar_barco(tablero, barco, fila, columna, orientacion, id_barco, demandas_filas, demandas_columnas):
    """
    Coloca o retira un barco en el tablero, eligiendo la dirección en función de las demandas.
    - Si es horizontal ('H'), elige extenderse a la derecha o izquierda según la demanda de columnas.
    - Si es vertical ('V'), elige extenderse hacia arriba o abajo según la demanda de filas.
    """
    n, m = tablero.shape

    if orientacion == 'H':
        # Comparar demandas a derecha e izquierda
        derecha_valida = columna + barco <= m and all(tablero[fila, columna:columna + barco] == 0)
        izquierda_valida = columna - barco + 1 >= 0 and all(tablero[fila, columna - barco + 1:columna + 1] == 0)

        demanda_derecha = sum(demandas_columnas[columna:columna + barco]) if derecha_valida else -1
        demanda_izquierda = sum(demandas_columnas[columna - barco + 1:columna + 1]) if izquierda_valida else -1

        if demanda_derecha >= demanda_izquierda and derecha_valida:
            for i in range(barco):
                tablero[fila][columna + i] = id_barco if id_barco != 0 else 0
        elif izquierda_valida:
            for i in range(barco):
                tablero[fila][columna - i] = id_barco if id_barco != 0 else 0

    elif orientacion == 'V':
        # Comparar demandas hacia abajo y hacia arriba
        abajo_valida = fila + barco <= n and all(tablero[fila:fila + barco, columna] == 0)
        arriba_valida = fila - barco + 1 >= 0 and all(tablero[fila - barco + 1:fila + 1, columna] == 0)

        demanda_abajo = sum(demandas_filas[fila:fila + barco]) if abajo_valida else -1
        demanda_arriba = sum(demandas_filas[fila - barco + 1:fila + 1]) if arriba_valida else -1

        if demanda_abajo >= demanda_arriba and abajo_valida:
            for i in range(barco):
                tablero[fila + i][columna] = id_barco if id_barco != 0 else 0
        elif arriba_valida:
            for i in range(barco):
                tablero[fila - i][columna] = id_barco if id_barco != 0 else 0


def sacar_barco(tablero, barco, fila, columna, orientacion, id_barco, demandas_filas, demandas_columnas):
    n, m = tablero.shape
    cambiados = 0
    for i in range(n):
        for j in range(m):
            if cambiados == barco:
                break
            if tablero[i][j] == id_barco:
                tablero[i][j] = 0
                cambiados += 1
                demandas_filas[i] += 1
                demandas_columnas[j] += 1


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


def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
    # Ordenar los barcos de mayor a menor longitud.
    barcos = sorted(barcos, reverse=True)
    demanda_cumplida_inicial = 0
    return batalla_naval_bt(tablero, demanda_cumplida_inicial, barcos, demandas_filas, demandas_columnas, 0, 0, tablero)


def batalla_naval_bt(tablero, demanda_cumplida, barcos, demandas_filas, demandas_columnas, indice, mejor_cumplida, mejor_tablero):
    # Caso base: todos los barcos han sido procesados.
    if demanda_cumplida > mejor_cumplida:
        mejor_cumplida = demanda_cumplida
        mejor_tablero = tablero.copy()

    if indice >= len(barcos):
        demanda_total = demandas_filas.sum() + demandas_columnas.sum()
        demanda_incumplida = demanda_total - demanda_cumplida
        if demanda_cumplida > mejor_cumplida:
            mejor_cumplida = demanda_cumplida
            mejor_tablero = tablero.copy()
            print(f"Nueva mejor solución encontrada:")
            print(tablero)
            print(f"Demanda cumplida: {demanda_cumplida}, Demanda incumplida: {demanda_incumplida}")
        return mejor_cumplida, mejor_tablero
    

    barco = barcos[indice]
    id_barco = indice + 1  # Identificador unico para el barco.

    # Obtener filas y columnas priorizadas.
    filas_prioritarias, columnas_prioritarias = obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas, tablero.copy())

    # Probar todas las combinaciones de posicion y orientacion.
    for fila in filas_prioritarias:
        if demandas_filas[fila] == 0: continue
        for columna in columnas_prioritarias:
            if demandas_columnas[columna] == 0: continue
            for orientacion in ['V', 'H']:
                if puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
                    # Colocar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, id_barco, demandas_filas, demandas_columnas)
                    demanda_cumplida = calcular_demanda_cumplida(tablero, demandas_filas, demandas_columnas)
                    #if demanda_cumplida >= mejor_cumplida:    
                    if demanda_cumplida > mejor_cumplida:
                        resultado_cumplido, resultado_tablero = batalla_naval_bt(tablero, demanda_cumplida, barcos, demandas_filas, demandas_columnas, indice + 1, mejor_cumplida, mejor_tablero)
                        if resultado_cumplido > mejor_cumplida:
                            mejor_cumplida = resultado_cumplido
                            mejor_tablero = resultado_tablero.copy()
                    # Retirar barco.
                    sacar_barco(tablero, barco, fila, columna, orientacion, id_barco, demandas_filas, demandas_columnas)

    return batalla_naval_bt(tablero, demanda_cumplida, barcos, demandas_filas, demandas_columnas, indice + 1, mejor_cumplida, mejor_tablero)

