import time
import numpy as np
import batalla_naval as bn

def generar_datos_prueba(filas, columnas, num_barcos):
    """
    Genera datos de prueba para el problema.
    - filas: Numero de filas del tablero.
    - columnas: Numero de columnas del tablero.
    - num_barcos: Número de barcos disponibles.
    Retorna:
    - tablero: Tablero vacio de tamaño filas x columnas.
    - barcos: Lista de tamanios de barcos.
    - demandas_filas: Lista de demandas de las filas.
    - demandas_columnas: Lista de demandas de las columnas.
    """
    np.random.seed(42)  # Fijar la semilla para reproducibilidad.

    tablero = np.zeros((filas, columnas), dtype=int)
    barcos = np.random.randint(1, min(filas, columnas) + 1, size=num_barcos)
    demandas_filas = np.random.randint(0, columnas + 1, size=filas)
    demandas_columnas = np.random.randint(0, filas + 1, size=columnas)

    return tablero, barcos, demandas_filas, demandas_columnas


# Generar datos de prueba.
tablero, barcos, demandas_filas, demandas_columnas = generar_datos_prueba(6, 6, 3)

# Ejecutar el algoritmo con barcos indivisibles.
inicio_tiempo = time.time()
demanda_final, tablero_final = bn.batalla_naval(tablero, barcos, demandas_filas, demandas_columnas)
fin_tiempo = time.time()

print(demanda_final, tablero_final, fin_tiempo - inicio_tiempo)