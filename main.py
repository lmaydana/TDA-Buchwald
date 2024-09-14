import n_monedas

def main():
    ruta = input("Ingrese ruta:")
    monedas = n_monedas.cargar_monedas_archivo(ruta)
    print(f"¿Ganó de Sophia?: {n_monedas.juego_sophia_mateo(monedas)}")

main()