import n_monedas

def main():
    ruta = input("Ingrese ruta:")
    monedas = n_monedas.cargar_monedas_archivo(ruta)
    monedas_sophia, monedas_mateo = n_monedas.juego_sophia_mateo(monedas)
    ganancia_sophia = sum(monedas_sophia)
    ganancia_mateo = sum(monedas_mateo)
    print(f"Ganancia Sophia: {ganancia_sophia}")
    print(f"Ganancia Mateo: {ganancia_mateo}")
    print(f"¿Ganó Sophia?: {ganancia_sophia > ganancia_mateo}")

main()