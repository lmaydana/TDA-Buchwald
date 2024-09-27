import n_monedas

def main():
    ruta = input("Ingrese ruta:")
    monedas = n_monedas.cargar_monedas_archivo(ruta)
    monedas_sophia, monedas_mateo = n_monedas.juego_sophia_mateo(monedas)
    print(n_monedas.devolver_jugadas(monedas_sophia, monedas_mateo))
    ganancia_sophia = n_monedas.devolver_ganancia(monedas, monedas_sophia)
    ganancia_mateo = n_monedas.devolver_ganancia(monedas, monedas_mateo)
    print(f"Ganancia Sophia: {ganancia_sophia}")
    print(f"Ganancia Mateo: {ganancia_mateo}")
    print(f"¿Ganó Sophia?: {ganancia_sophia > ganancia_mateo}")

main()