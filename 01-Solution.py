#!/usr/bin/env python3.10


lines, largo=[], []
with open("input01.txt") as file_object:
  lines = file_object.readlines()

for line in lines: 
  largo.append(line.rstrip())

corto="""1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""".split("\n")


class Calorias:
    def mayor_suma(lista_calorias):
        elfo_con_mas_calorias = 0
        calorias_de_elfo = 0
        for renglon in lista_calorias:
            if renglon != "":
                calorias_de_elfo += int(renglon)
            else:
                calorias_de_elfo = 0 
            elfo_con_mas_calorias = max(elfo_con_mas_calorias, calorias_de_elfo)
        return elfo_con_mas_calorias

    def mayores_tres_suma(lista_calorias):
        lista_calorias.append("")
        maximo, calorias_de_elfo, lista_total_calorias_de_elfo = 0,0,[]
        for renglon in lista_calorias:
            if renglon != "":
                calorias_de_elfo += int(renglon)
            else:
                lista_total_calorias_de_elfo.append(calorias_de_elfo)
                calorias_de_elfo = 0
        lista_total_calorias_de_elfo.sort()
        return sum(lista_total_calorias_de_elfo[-3:])


assert Calorias.mayor_suma(corto)==24000
assert Calorias.mayores_tres_suma(corto)==45000
print("	La respuesta A es " + str(Calorias.mayor_suma(largo)))
print("	La respuesta B es " + str(Calorias.mayores_tres_suma(largo)))
