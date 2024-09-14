import sys

sys.setrecursionlimit(100000)

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

    while monedas:
        if es_turno_de_sophia:
            moneda = monedas.pop(posicion_moneda(monedas, maximo=True))
            monedas_sophia.append(moneda)
        else:
            moneda = monedas.pop(posicion_moneda(monedas, maximo=False))
            monedas_mateo.append(moneda)
        es_turno_de_sophia = not es_turno_de_sophia

    sumatoria_sophia = sum(monedas_sophia)
    sumatoria_mateo = sum(monedas_mateo)
    return sumatoria_sophia

def posicion_moneda(monedas, maximo):
    if maximo:
        if monedas[0] >= monedas[len(monedas) - 1]:
            return 0
        return len(monedas) - 1
    else:
        if monedas[0] < monedas[len(monedas) - 1]:
            return 0
        return len(monedas) - 1