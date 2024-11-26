import numpy as np

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
                    demandas_filas_cop[fila] - barco >= 0 and \
                    all(demandas_columnas_cop[j] - 1 >= 0 for j in range(columna, columna + barco)):
                # Verificar adyacencia
                if all(tablero_cop[max(0, fila - 1):min(filas, fila + 2), max(0, columna - 1):min(columnas, columna + barco + 1)].flatten() == 0):
                    return True


    elif orientacion == 'V':  # Vertical
        # Verificar hacia abajo
        if fila + barco <= filas:
            if all(tablero_cop[fila:fila + barco, columna] == 0) and \
                    demandas_columnas_cop[columna] - barco >= 0 and \
                    all(demandas_filas_cop[i] - 1 >= 0 for i in range(fila, fila + barco)):
                # Verificar adyacencia
                if all(tablero_cop[max(0, fila - 1):min(filas, fila + barco + 1), max(0, columna - 1):min(columnas, columna + 2)].flatten() == 0):
                    return True


    return False


def colocar_barco(tablero, barco, fila, columna, orientacion, id_barco, demandas_fila, demandas_columna):
    """
    Coloca o retira un barco en el tablero, eligiendo la direccion.
    - Si es horizontal ('H'), elige extenderse a la derecha.
    - Si es vertical ('V'), elige extenderse hacia abajo.
    """
    if orientacion == 'H':
        for i in range(barco):
            tablero[fila][columna + i] = id_barco
            if id_barco != 0:
                demandas_columna[columna + i] -= 1
            else:
                demandas_columna[columna + i] += 1
        if id_barco != 0:
            demandas_fila[fila] -= barco
        else:
            demandas_fila[fila] += barco

    elif orientacion == 'V':
        for i in range(barco):
            tablero[fila + i][columna] = id_barco 
            if id_barco != 0:
                demandas_fila[fila + i] -= 1
            else:
                demandas_fila[fila + i] += 1
        if id_barco != 0:
            demandas_columna[columna] -= barco
        else:
            demandas_columna[columna] += barco


def obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas, tablero):
    """
    Obtiene listas de filas y columnas priorizadas por demanda restante absoluta (mayor urgencia).
    """
    # Priorizar por la demanda restante absoluta.
    filas_prioritarias = np.argsort(-demandas_filas).tolist() # Devuelve los indices.
    columnas_prioritarias = np.argsort(-demandas_columnas).tolist()

    print(f"Filas prioritarias: {filas_prioritarias}")
    print(f"Columnas prioritarias: {columnas_prioritarias}")

    return filas_prioritarias, columnas_prioritarias


def batalla_naval(tablero, barcos, demandas_filas, demandas_columnas):
    # Ordenar los barcos de mayor a menor longitud.
    barcos = sorted(barcos, reverse=True)
    demanda_total = demandas_filas.sum() + demandas_columnas.sum()
    sol_optima = [demanda_total, tablero.copy(), 0]
    sol_parcial = [demanda_total, tablero, 0] #[demanda incumplida, tablero]

    batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, 0, sol_parcial, sol_optima)
    return demanda_total - sol_optima[0], sol_optima[1]


def batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, indice, sol_parcial, sol_optima):
    
    if indice >= len(barcos):
        if sol_parcial[0] < sol_optima[0]:
            sol_optima[0] = sol_parcial[0]
            sol_optima[1] = sol_parcial[1].copy()
        return

    if sol_parcial[0] < sol_optima[0]:
        sol_optima[0] = sol_parcial[0]
        sol_optima[1] = sol_parcial[1].copy()

    if demandas_filas.sum() + demandas_columnas.sum() - (sum(barcos[indice:])*2) >= sol_optima[0]:
        return

    barco = barcos[indice]
    id_barco = indice + 1  # Identificador unico para el barco.

    # Obtener filas y columnas priorizadas.
    filas_prioritarias, columnas_prioritarias = obtener_filas_columnas_prioritarias(demandas_filas, demandas_columnas, tablero.copy())

    cota_superior = sum(max(0, d - barco) for d in demandas_filas) + sum(max(0, d - barco) for d in demandas_columnas)
    """Esto seria lo que mas podria abarcar el barco, dejando la sumatoria de demandas restastenes en fila y columna"""
    if cota_superior >= sol_optima[0]:
        return

    # Probar todas las combinaciones de posicion y orientacion.
    for fila in filas_prioritarias:
        if demandas_filas[fila] == 0: continue
        for columna in columnas_prioritarias:
            if demandas_columnas[columna] == 0: continue
            for orientacion in ['H', 'V']:
                if puede_colocar_barco(tablero, barco, fila, columna, orientacion, demandas_filas, demandas_columnas):
                    # Colocar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, id_barco, demandas_filas, demandas_columnas)

                    sol_parcial[0] = demandas_filas.sum() + demandas_columnas.sum()
                    sol_parcial[1] = tablero.copy()

                    if sol_parcial[0] < sol_optima[0] or sol_parcial[0] - (sum(barcos[indice:])*2) < sol_optima[0]:
                        batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, indice + 1, sol_parcial, sol_optima)
                    # Retirar barco.
                    colocar_barco(tablero, barco, fila, columna, orientacion, 0, demandas_filas, demandas_columnas)

    return batalla_naval_bt(tablero, barcos, demandas_filas, demandas_columnas, indice + 1, sol_parcial, sol_optima)
