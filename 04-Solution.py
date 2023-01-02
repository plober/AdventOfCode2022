#!/usr/bin/env python3.10


lines, largo=[], []
with open("input04.txt") as file_object:
  lines = file_object.readlines()

for line in lines: 
  largo.append(line.rstrip())


corto="""2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".splitlines()

class CampCleanup:
    def uno_contenido_en_otro(tramos):
        # [intervalos for intervalos in [par.split(",") for par in corto]]
        contenidos_encontrados=0
        for par in tramos:
            # par = "5-7,7-9"
            par.replace(",","-")
            # par = "5-7-7-9"
            menor_1, mayor_1, menor_2, mayor_2 = [int(valor) for valor in par.replace(",","-").split("-")]

            if [menor_1, mayor_1] == [menor_2, mayor_2]:
                contenidos_encontrados += 1
                continue
                        
            if menor_1 <= menor_2 and mayor_2 <= mayor_1:
                contenidos_encontrados += 1
                
            if menor_2 <= menor_1 and mayor_1 <= mayor_2:
                contenidos_encontrados += 1
        return contenidos_encontrados
            
    def hay_intersecciones(tramos):
        intersecciones_encontradas=0
        for par in tramos:
            par.replace(",","-")
            menor_1, mayor_1, menor_2, mayor_2 = [int(valor) for valor in par.replace(",","-").split("-")]
            if len(set(range(menor_1, mayor_1+1)) & set(range(menor_2, mayor_2+1))) > 0: 
                intersecciones_encontradas += 1
        return intersecciones_encontradas
 
respuesta_corta_a = CampCleanup.uno_contenido_en_otro(corto)
respuesta_larga_a = CampCleanup.uno_contenido_en_otro(largo)
assert respuesta_corta_a==2, \
    f"Resultado no condice con el ejemplo, obtuve {str(respuesta_corta_a)}"
print("	La respuesta A es " + str(respuesta_larga_a))

respuesta_corta_b = CampCleanup.hay_intersecciones(corto)
respuesta_larga_b = CampCleanup.hay_intersecciones(largo)
assert respuesta_corta_b==4, \
    f"Resultado no condice con el ejemplo, obtuve {str(respuesta_corta_b)}"
print("	La respuesta B es " + str(respuesta_larga_b))
