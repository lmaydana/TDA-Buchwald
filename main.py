import sys
import n_monedas

sys.setrecursionlimit(100000)

def main():
    ruta = "pruebas/20000.txt"     #  sys.argv[:]
    monedas = n_monedas.cargar_monedas_archivo(ruta)
    print(n_monedas.juego_sophia_mateo(monedas))
    #return
main()