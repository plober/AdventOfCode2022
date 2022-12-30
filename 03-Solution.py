#!/usr/bin/env python3.10


lines, largo=[], []
with open("input03.txt") as file_object:
  lines = file_object.readlines()

for line in lines: 
  largo.append(line.rstrip())


corto="""vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".splitlines()


class ItemsMochila:

    def numero_letra(caracter): 
        return ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(caracter)

    def repetidos_mitades(string_items):
        return set(string_items[:len(string_items)//2]) & set(string_items[len(string_items)//2:])
    
    def suma_repetidos(inventarios):
        total = 0
        for lista in inventarios:
            total += ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.find((set(lista[:len(lista)//2]) & set(lista[len(lista)//2:])).pop())
        return total
    
    def repetido_en_tres(triplete):
        [elfo_1, elfo_2, elfo_3] = triplete
        return set(elfo_1) & set(elfo_2) & set(elfo_3)

    def suma_tripletes(lista):
        suma_total = 0
        for numero in range (0,len(lista),3):
            repetido=set(lista[numero]) & set(lista[numero+1]) & set(lista[numero+2])
            suma_total += ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(repetido.pop())
            # print(suma_total)
        return suma_total

            
assert ItemsMochila.repetidos_mitades(corto[0]).pop()=='p'
assert ItemsMochila.repetidos_mitades(corto[1]).pop()=='L'
assert ItemsMochila.repetidos_mitades(corto[2]).pop()=='P'
assert ItemsMochila.repetidos_mitades(corto[3]).pop()=='v'
assert ItemsMochila.repetidos_mitades(corto[4]).pop()=='t'
assert ItemsMochila.repetidos_mitades(corto[5]).pop()=='s'
 
assert ItemsMochila.suma_repetidos(corto)== 157
RespuestaA, RespuestaB = ItemsMochila.suma_repetidos(largo), 'N/A'

print("	La respuesta A es " + str(RespuestaA))

assert ItemsMochila.repetido_en_tres(corto[:3]).pop()=='r'
assert ItemsMochila.repetido_en_tres(corto[3:][:3]).pop()=='Z'

print("	La respuesta B es " + str(ItemsMochila.suma_tripletes(largo)))
