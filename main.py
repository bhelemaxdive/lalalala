from typing import List, Tuple

# Bloques según la ruleta europea
bloque_P = {32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13}
bloque_Q = {36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20}
bloque_R = {14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26}

# === Estado global ===
sec_bloques: List[Tuple[int, str]] = []
tabla = []
base = []
anterior_bloque = None
saldo = 0
saldo_30 = 0
tiros_30 = 0
aciertos = 0
fallos = 0
paso = 0

def numero_a_bloque(n):
    if n == 0:
        return '[0]'
    elif n in bloque_P:
        return 'P'
    elif n in bloque_Q:
        return 'Q'
    elif n in bloque_R:
        return 'R'
    else:
        return '???'

def procesar_numero(num: int):
    global paso, anterior_bloque, base, saldo, saldo_30, tiros_30, aciertos, fallos
    bloque = numero_a_bloque(num)
    sec_bloques.append((num, bloque))

    resultado_valor = 0

    if bloque == '???':
        resultado_valor = 0
        tabla.append([paso, num, bloque, base.copy(), "❌ Inválido", "0", None, resultado_valor, saldo_30])
        paso += 1
        return

    if bloque == '[0]':
        resultado_valor = 1
        saldo += 1
        aciertos += 1
        saldo_30 += resultado_valor
        tiros_30 += 1
        tabla.append([paso, num, bloque, base.copy(), "✅ Comodín", "+1", base.copy(), resultado_valor, saldo_30])
        paso += 1
        return

    if not base and anterior_bloque is not None and anterior_bloque != bloque:
        base = [anterior_bloque, bloque]
        resultado_valor = 0
        tabla.append([paso, num, bloque, "—", "⏳ Base inicial", "0", base.copy(), resultado_valor, saldo_30])
        anterior_bloque = bloque
        paso += 1
        return

    if bloque in base:
        resultado_valor = 1
        saldo += 1
        aciertos += 1
        tabla.append([paso, num, bloque, base.copy(), "✅ Sí", "+1", base.copy(), resultado_valor, 0])
    else:
        resultado_valor = -2
        saldo -= 2
        fallos += 1
        tabla.append([paso, num, bloque, base.copy(), "❌ No", "-2", None, resultado_valor, 0])
        if anterior_bloque and anterior_bloque != bloque:
            base = [anterior_bloque, bloque]
        else:
            base = [bloque]
        tabla[-1][6] = base.copy()

    anterior_bloque = bloque
    saldo_30 += resultado_valor
    tiros_30 += 1

    tabla[-1][-1] = saldo_30

    if tiros_30 == 30:
        saldo_30 = 0
        tiros_30 = 0

    paso += 1

def mostrar_tabla():
    for fila in tabla:
        print(fila)
    print(f"\n✅ Aciertos: {aciertos}")
    print(f"❌ Fallos: {fallos}")
    print(f"💰 Saldo final: {saldo}")

def cargar_secuencia_inicial(numeros: List[int]):
    for num in numeros:
        procesar_numero(num)
    mostrar_tabla()

def bucle_interactivo():
    print("\n🔄 Ahora puedes ingresar nuevos números uno por uno. Escribe 'salir' para terminar.")
    while True:
        entrada = input("👉 Ingrese número: ").strip()
        if entrada.lower() in ['salir', 'x', 'exit']:
            print("👋 Sesión finalizada.")
            break
        if not entrada.isdigit():
            print("❌ Entrada inválida.")
            continue
        numero = int(entrada)
        if not (0 <= numero <= 36):
            print("❌ Número fuera de rango.")
            continue
        procesar_numero(numero)
        mostrar_tabla()

# === Inicio general ===
if __name__ == "__main__":
    respuesta = input("¿Deseas cargar una secuencia de números? (s/n): ").strip().lower()
    if respuesta == 's':
        print("🔢 Pega la secuencia separada por comas (ej: 1,2,3,...):")
        numeros_str = input("👉 ")
        lista_base = [int(x.strip()) for x in numeros_str.split(',') if x.strip().isdigit()]
        cargar_secuencia_inicial(lista_base)

    # Siempre entra al modo interactivo
    bucle_interactivo()
