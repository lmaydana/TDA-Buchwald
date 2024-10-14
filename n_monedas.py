import sys

def cargar_monedas_archivo(ruta):
    monedas = []
    with open(ruta) as file:
        next(file)
        for linea in file:
            valores = linea.split(";")
            for valor in valores:
                monedas.append(int(valor))
    return monedas

def juego_sophia_mateo(monedas):
    cant_monedas = len(monedas)
    
    matriz = [[0] * cant_monedas for _ in range(cant_monedas)]
    
    # Caso base: cuando solo hay una moneda (Sophia toma la unica moneda)
    for i in range(cant_monedas):
        matriz[i][i] = monedas[i]
    
    # Vamos llenando la tabla desde casos menores.
    for longitud in range(2 + cant_monedas % 2, cant_monedas + 1, 2):
        for ini in range(cant_monedas - longitud + 1):
            fin = ini + longitud - 1
            
            # Sophia toma la moneda en el extremo izquierdo
            opcion_izquierda = monedas[ini]
            # Sumamos valores dependiendo de la decision de Mateo
            if monedas[ini + 1] > monedas[fin]:
                opcion_izquierda += matriz[ini + 2][fin] if ini + 2 <= fin else 0
            else:
                opcion_izquierda += matriz[ini + 1][fin - 1] if ini + 1 <= fin - 1 else 0 

            # Mismo procedimiemto pero para la moneda del extremo derecho
            opcion_derecha = monedas[fin]
           
            if monedas[ini] > monedas[fin - 1]:
                opcion_derecha += matriz[ini + 1][fin - 1] if ini + 1 <= fin - 1 else 0  
            else:
                opcion_derecha += matriz[ini][fin - 2] if ini <= fin - 2 else 0
            
            # Guardar el valor maximo en matriz
            matriz[ini][fin] = max(opcion_izquierda, opcion_derecha)
    
    return rearmar_solucion(matriz, monedas)

def rearmar_solucion(matriz, monedas):
    solucion_sophia = []
    solucion_mateo = []
    cant_monedas = len(monedas)
    ini = 0
    fin = cant_monedas - 1
    valor_maximo = matriz[ini][fin]
    while valor_maximo > 0:
        if ini == fin:
            solucion_sophia.append(ini)
            break
        siguiente_ini, siguiente_fin = siguientes_indices_eligiendo_mateo(ini + 1, fin, monedas)
        if valor_maximo == monedas[ini] + matriz[siguiente_ini][siguiente_fin]:
            solucion_sophia.append(ini)
            valor_maximo -= monedas[ini]
            if siguiente_ini == ini + 1:
                solucion_mateo.append(fin)
            else:
                solucion_mateo.append(ini + 1)
        else:
            siguiente_ini, siguiente_fin = siguientes_indices_eligiendo_mateo(ini, fin - 1, monedas)
            solucion_sophia.append(fin)
            valor_maximo -= monedas[fin]
            if siguiente_ini == ini:
                solucion_mateo.append(fin - 1)
            else:
                solucion_mateo.append(ini)
        ini = siguiente_ini
        fin = siguiente_fin
    return solucion_sophia, solucion_mateo


def siguientes_indices_eligiendo_mateo(ini, fin, monedas):
    if monedas[fin] >= monedas[ini]:
        return ini, fin - 1
    else: 
        return ini + 1, fin

def devolver_ganancia(monedas, monedas_jugador):
    ganancia = 0
    for indice in monedas_jugador:
        ganancia += monedas[indice]
    return ganancia
def devolver_jugadas(monedas_sophia, monedas_mateo):
    juego = ""
    primera = 0
    ultima = len(monedas_sophia) + len(monedas_mateo) - 1
    for i in range(len(monedas_mateo)):
        moneda_sophia = monedas_sophia[i]
        moneda_mateo = monedas_mateo[i]
        elegida_mateo = "Última"
        elegida_sophia = "Última"
        if moneda_sophia == primera:
            elegida_sophia = "Primera"
            primera += 1
        else:
            ultima -= 1
        if moneda_mateo == primera:
            elegida_mateo = "Primera"
            primera +=1
        else:
            ultima -= 1
        juego+=f"{elegida_sophia} moneda para Sophia; {elegida_mateo} moneda para Mateo; "
    if len(monedas_sophia) > len(monedas_mateo):
        juego+=f"Última moneda para Sophia"
    return juego