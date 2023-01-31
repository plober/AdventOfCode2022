#!/usr/bin/env python3.10


largo = [line.rstrip() for line in open("input13.txt")]

corto = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".splitlines()

# [(numero, numero+1) for numero in range(0, len(corto), 3)]


class DistressSignal:

    def __init__(self, señal):
        self.señal = señal

        self.comparables = [(eval(señal[posteo[0]]), eval(señal[posteo[1]])) for posteo in [
            (numero, numero+1) for numero in range(0, len(señal), 3)]]

        self.señal_a_ordenar =  [eval(linea) for linea in señal if linea != ''] +[[[2]]] + [[[6]]]

    def par_en_orden_correcto(self, renglon1, renglon2):
        return self.compara_solo_enteros(renglon1, renglon2)

    def respuesta_final(self, vidente = False) -> int:
        rta_comparada = """True 
True 
False
True 
False
True 
False
False""".splitlines()
        if vidente:
            for valor, dupla in enumerate(self.comparables):
                comparado = self.compara(dupla[0], dupla[1])
                print("{} * {:<5s} = {} {}".format(valor+1, str(comparado), (valor+1) * comparado,
                    f"deberia ser {rta_comparada[valor]}" if eval(rta_comparada[valor]) != comparado else ""))
                # {:~<9s}

        respuesta = sum((valor+1) * self.compara(dupla[0], dupla[1]) 
                        for valor, dupla in enumerate(self.comparables))
        return respuesta

    def compara(self, izquierda, derecha) -> bool | None:
        """Devuelve el booleano de si el primer término de la tupla es menor que el segundo,
        solucionando problema de tipos"""
        if izquierda != derecha:
            tipos = (type(izquierda), type(derecha))
            if tipos == (int, int):     return self.compara_solo_enteros(izquierda, derecha)
            elif tipos == (int, list):  return self.compara([izquierda], derecha)
            elif tipos == (list, int):  return self.compara(izquierda, [derecha])
            elif tipos == (list, list): return self.compara_solo_listas(izquierda, derecha)


    def compara_solo_listas(self, izquierda, derecha) -> bool | None:
        """Toma dos listas y compara elemento por elemento.
        Devuelve F al primer imbalance.
        Devuelve T si se mantuvo el balance y la primer lista es la más corta
        Devuelve F si la 2nda lista es más larga"""
        # If both values are lists, compare the first value of each list, then the second value, and so on.
        # Return result as sooon as a difference appears
        # If the left list runs out of items first, the inputs are in the right order.
        # If the right list runs out of items first, the inputs are not in the right order.
        minimo = min(len(izquierda), len(derecha))
        for termino in range(minimo):
            igualdad = self.compara(izquierda[termino], derecha[termino])
            if igualdad == True:    return True
            if igualdad == False:   return False
        if len(izquierda) < len(derecha): return True
        if len(izquierda) > len(derecha): return False
        # Si la primera lista es más corta que la segunda, califica. Si n, tiene que continuar

    def compara_solo_enteros(self, izquierda: int, derecha: int) -> bool | None:
        """Devuelve el booleano de si el primer elemento es menor que el segundo"""
        # If both values are integers, the lower integer should come first.
        # If the inputs are the same integer; continue checking the next part of the input.
        if izquierda < derecha: return True
        if izquierda > derecha: return False

##############################
    def particion(self, lista: list, bajo: int, alto: int):
    # choose the rightmost element as pivot
        pivote = lista[alto]
        # pointer for greater element
        indice_mayor = bajo - 1
        # traverse through all elements
        # compare each element with pivot
        for indice_menor in range(bajo, alto):
            if self.compara(lista[indice_menor], pivote):
                # If element smaller than pivot is found
                # swap it with the greater element pointed by indice_mayor
                indice_mayor = indice_mayor + 1
                # Swapping element at indice_mayor with element at j
                lista[indice_mayor], lista[indice_menor] = lista[indice_menor], lista[indice_mayor]
        # Swap the pivot element with the greater element specified by indice_mayor
        lista[indice_mayor + 1], lista[alto] = lista[alto], lista[indice_mayor + 1]
        # Return the position from where partition is done
        # for linea in lista: print(linea)
        # print("-"*5)
        return indice_mayor + 1
 
# function to perform quicksort
 
    def quickSort(self, lista: list, bajo:int, alto:int):
        if bajo < alto:
            # Find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = self.particion(lista, bajo, alto)
            # Recursive call on the left of pivot
            self.quickSort(lista, bajo, pi - 1)
            # Recursive call on the right of pivot
            self.quickSort(lista, pi + 1, alto)
#############################

    def ordena(self):
        tamaño = len(self.señal_a_ordenar)
        self.quickSort(self.señal_a_ordenar, 0, tamaño - 1)
    
    def respuesta_B(self) -> int:
        return (self.señal_a_ordenar.index([[2]])+1) * (self.señal_a_ordenar.index([[6]])+1)


rta_corta = DistressSignal(corto)
# for comparo in rta_corta.comparables: print(f"{comparo[0]}\n{comparo[1]}\n---------\n")
print(rta_corta.respuesta_final(vidente = True))

assert rta_corta.compara(0, 1) == True, f"No compara bien número enteros"
assert rta_corta.compara(6, 1) == False, f"No compara bien número enteros"
assert rta_corta.compara([], [[], []]) == True, f"No compara bien tamaños de listas (para True)"
assert rta_corta.compara([[]], [[], []]) == True, f"No compara bien tamaños de listas (para True)"
assert rta_corta.compara([[], []], []) == False, f"No compara bien tamaños de listas (para False)"
assert rta_corta.compara([6, []], [7]) == True, f"No está comparando bien"
assert rta_corta.compara([8, []], [7]) == False, f"No está comparando bien"
assert rta_corta.compara([2, []], [7, [], []]) == True, f"No está comparando bien"

print("-- parte B --\n")
rta_corta.ordena()
for linea in rta_corta.señal_a_ordenar: print(linea)
print(f"Respuesta B: {rta_corta.respuesta_B()}")

rta_larga = DistressSignal(largo)
rta_larga.ordena()

RespuestaA, RespuestaB = rta_larga.respuesta_final(), rta_larga.respuesta_B()


print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
