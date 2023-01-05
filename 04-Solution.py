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

contenidos_encontrados=[]

class CampCleanup:
    def uno_contenido_en_otro(tramos):
        """ Devuelve la cantidad de renglones que muestran que iun rango está completamente dentro de otro.
        Todo rango se contiene a sí mismo"""
        # [intervalos for intervalos in [par.split(",") for par in corto]]
        cantidad_encontrados=0
        for par in tramos:
            # par = "5-7,7-9"
            # par.replace(",","-")
            # par = "5-7-7-9"
            menor_1, mayor_1, menor_2, mayor_2 = [int(valor) for valor in par.replace(",","-").split("-")]

            if [menor_1, mayor_1] == [menor_2, mayor_2]:
                cantidad_encontrados += 1
                contenidos_encontrados.append(par)
                continue
                        
            if menor_1 <= menor_2 and mayor_2 <= mayor_1:
                cantidad_encontrados += 1
                contenidos_encontrados.append(par)                
                
            if menor_2 <= menor_1 and mayor_1 <= mayor_2:
                cantidad_encontrados += 1
                contenidos_encontrados.append(par)
        return cantidad_encontrados

    def uno_contenido_en_otro_oneliner(tramos):
        """Premature Optimization Is the Root of All Evil"""

        final = [menor_1 for (menor_1, mayor_1, menor_2, mayor_2) in [terna.replace(",","-").split("-") for terna in tramos] \
             if (int(menor_1) <= int(menor_2) and int(mayor_2) <= int(mayor_1)) \
             or (int(menor_2) <= int(menor_1) and int(mayor_1) <= int(mayor_2))]
        # TODO: ¿Cómo hago para mandarles el Int directamente? 
        # print("  Oneliner:")
        # for line in final[:2]:
        #     print("{}-{},{}-{}".format(line[0], line[1], line[2], line[3]))
        
        # rta_oneliner =[]
        # for line in final:
        #     rta_oneliner.append("{}-{},{}-{}".format(line[0], line[1], line[2], line[3]))

        # print("  Oficial:")
        # for line in contenidos_encontrados[:2]:
        #     print(line)
        
        # print("  Diferencia:")
        # for line in set(rta_oneliner)-set(contenidos_encontrados):
        #     print(line)


        return len(final)

            
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
print(" Me hago el vivo: {}".format(CampCleanup.uno_contenido_en_otro_oneliner(largo)))
