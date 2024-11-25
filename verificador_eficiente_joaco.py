"""
La idea de un verificador eficiente debe ser que dada una solucion a un problema, se corobore de manera polinomia
si esa solucion es valida o no.
Para este caso tendremos en cuenta la consigna de:
Dado un tablero de nxm casilleros, y una lista de k barcos (donde el barco i tiene bi de largo), una lista de 
restricciones para las filas (donde la restricción j corresponde a la cantidad de casilleros a ser ocupados en 
la fila j) y una lista de restricciones para las columnas (símil filas, pero para columnas), ¿es posible definir 
una ubicación de dichos barcos de tal forma que se cumplan con las demandas de cada fila y columna, y las 
restricciones de ubicación?
"""

def verificador_eficiente(tablero_solucion, barcos, demandas_filas, demandas_columnas):
    """
    Pre: Recibe:
    - Un tablero con los barcos ubicados como solucion (siendo 0 espacios libres y numeros los barcos).
    - Lista de barcos original.
    - Lista de demandas de filas original.
    - Lista de demandas de columnas original.

    Debemos validar que la solucion:
    - Cubra todas las demandas de filas y columnas (ni mas ni menos).
    - Los barcos cumplan con la ley de adyacencia.
    """

    demanda_restante = calcular_demandas_restantes(tablero_solucion, demandas_filas, demandas_columnas)
    if demanda_restante != 0:
        return False
    
    n, m = tablero_solucion.shape
    barcos_checkeados = set()

    for fila in range(len(tablero_solucion)):
        for columna in range(len(tablero_solucion[0])):
            if tablero_solucion[fila][columna] != 0 and not tablero_solucion[fila][columna] in barcos_checkeados:
                barco = tablero_solucion[fila][columna]
                barco_largo = barcos[barco-1]

                if barco > 1:
                    # Si el barco no es de un solo bloque de largo.
                    if columna < m and tablero_solucion[fila][columna + 1] == barco:
                        if not se_puede_colocar(tablero_solucion, barco, barco_largo, fila, columna, "H"):
                            return False
                        
                    if fila < n and tablero_solucion[fila + 1][columna] == barco:
                        if not se_puede_colocar(tablero_solucion, barco, barco_largo, fila, columna, "V"):
                            return False
                        
                else:
                    if not se_puede_colocar(tablero_solucion, barco, barco_largo, fila, columna, None):
                        return False
                    
                barcos_checkeados.add(barco)
    
    return True


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


def se_puede_colocar(tablero, barco, barco_largo, fila, columna, orientacion):

    filas, columnas = tablero.shape

    if orientacion == 'H':  # Horizontal.
        # Verificar hacia la derecha.
        if columna + barco_largo <= columnas:
            if all(tablero[fila, columna:columna + barco_largo] == barco):
                # Verificar adyacencia.
                if all(tablero[max(0, fila - 1):min(filas, fila + 2), max(0, columna - 1):min(columnas, columna + barco + 1)].flatten() == 0):
                    return True

    elif orientacion == 'V':  # Vertical.
        # Verificar hacia abajo.
        if fila + barco_largo <= filas:
            if all(tablero[fila:fila + barco_largo, columna] == barco):
                # Verificar adyacencia.
                if all(tablero[max(0, fila - 1):min(filas, fila + barco_largo + 1), max(0, columna - 1):min(columnas, columna + 2)].flatten() == 0):
                    return True
    
    elif not orientacion:
        # Verificar adyacencia.
        if all(tablero[max(0, fila - 1):min(filas, fila + 2), max(0, columna - 1):min(columnas, columna + 2)].flatten() == 0):
            return True

    return False
