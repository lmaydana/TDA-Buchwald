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
    monedas_sophia = []
    monedas_mateo = []
    es_turno_de_sophia = True
    ini = 0
    fin = len(monedas) - 1
    while ini <= fin:
        monedas_jugador = monedas_sophia
        posicion_moneda_a_agregar = posicion_moneda(monedas, ini, fin, maximo=es_turno_de_sophia)
        if not es_turno_de_sophia:
            monedas_jugador = monedas_mateo
        monedas_jugador.append(posicion_moneda_a_agregar)
        if posicion_moneda_a_agregar == fin:
            fin -= 1
        else:
            ini += 1
        es_turno_de_sophia = not es_turno_de_sophia

    return monedas_sophia, monedas_mateo

def posicion_moneda(monedas, ini, fin, maximo):
    if maximo:
        if monedas[ini] >= monedas[fin]:
            return ini
        return fin
    else:
        if monedas[ini] < monedas[fin]:
            return ini
        return fin