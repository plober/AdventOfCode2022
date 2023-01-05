#!/usr/bin/env python3.10

lines, largo=[], []
with open("input05.txt") as file_object:
  lines = file_object.readlines()

for line in lines:
  largo.append(line.rstrip())



corto_texto="""    [D]
[N] [C]
[Z] [M] [P]
 1   2   3 """

corto_inicial =[]
for line in corto_texto.split('\n'):
   corto_inicial.append(line.rstrip())
largo_inicial = largo[:9]

   # cortoInicial= ["       [D]",
   #                "   [N] [C]",
   #                "   [Z] [M] [P]",
   #                "    1   2   3 "]

corto_movimientos=[  "move 1 from 2 to 1",
                    "move 3 from 1 to 3",
                    "move 2 from 2 to 1",
                    "move 1 from 1 to 2"]
largo_movimientos=largo[10:]
# Stacks Página 615

class Inputs:
    def parseo_situacion(situacion):
        #[x for x in beta if x not in "[]"][::2]
        situacion.reverse()
        renglones = len (situacion)
        largo = len (situacion[0])
        diccionario_pilas = {}
        traspuesto=""
        for caracter_columna in range(len(situacion[0]))[1::4]:
            traspuesto = ['{: <{}}'.format(fila,largo)[caracter_columna] for fila in situacion]
            diccionario_pilas[int(traspuesto[0])] = ''.join(traspuesto[1:]).strip()
        return diccionario_pilas

    def parseo_movimientos(movimientos):
        actividad=[]
        for linea in movimientos:
            # _, uno, _, dos, _, tres = linea.split()
            # Mejor
            # uno, dos, tres = linea.split()[1::2]
            # actividad.append([int(uno), int(dos), int(tres)])
            # Mucho mejor
            actividad.append([int(valor) for valor in linea.split()[1::2]])

        return actividad

class Respuesta:
    def ejecucion_movimientos(diccionario_pilas, instrucciones):
        # Mueve de a uno
        for comando in instrucciones:
            # comando = "move 3 from 1 to 3" -> [3,1,3]
            [cuantos, desde, hacia] = comando
            #"move {} from {} to {}".format(cuantos, desde, hacia)
            for _ in range(cuantos):
                diccionario_pilas[hacia] = diccionario_pilas[hacia] + diccionario_pilas[desde][-1]
                diccionario_pilas[desde] = diccionario_pilas[desde][:-1]
        return ''.join([valor[-1] for valor in diccionario_pilas.values()])

    def ejecucion_movimientos_b(diccionario_pilas, instrucciones):
        # Mueve todos juntos
        print(diccionario_pilas)
        for comando in instrucciones:
            [cuantos, desde, hacia] = comando
            diccionario_pilas[hacia] = diccionario_pilas[hacia] + diccionario_pilas[desde][-cuantos:]
            diccionario_pilas[desde] = diccionario_pilas[desde][:-cuantos]
        return ''.join([valor[-1] for valor in diccionario_pilas.values()])


#        for comando in instrucciones:

respuesta_corta_a = Respuesta.ejecucion_movimientos(Inputs.parseo_situacion(corto_inicial.copy()),Inputs.parseo_movimientos(corto_movimientos.copy()))
respuesta_a = Respuesta.ejecucion_movimientos(Inputs.parseo_situacion(largo_inicial.copy()),Inputs.parseo_movimientos(largo_movimientos.copy()))
respuesta_corta_b = Respuesta.ejecucion_movimientos_b(Inputs.parseo_situacion(corto_inicial.copy()),Inputs.parseo_movimientos(corto_movimientos.copy()))
respuesta_b = Respuesta.ejecucion_movimientos_b(Inputs.parseo_situacion(largo_inicial.copy()),Inputs.parseo_movimientos(largo_movimientos.copy()))

assert Inputs.parseo_situacion(corto_inicial.copy()) == {1:"ZN",2:"MCD", 3:"P"}
assert Inputs.parseo_movimientos(corto_movimientos.copy()) == [[1,2,1],[3,1,3],[2,2,1],[1,1,2]]
assert Respuesta.ejecucion_movimientos(Inputs.parseo_situacion(corto_inicial.copy()),Inputs.parseo_movimientos(corto_movimientos.copy())) == "CMZ"
print("	La respuesta del Ejemplo A es " + str(respuesta_corta_a))
print("	La respuesta A es " + str(respuesta_a))

assert Respuesta.ejecucion_movimientos_b(Inputs.parseo_situacion(corto_inicial.copy()),Inputs.parseo_movimientos(corto_movimientos.copy())) == "MCD"

print("	La respuesta del Ejemplo B es " + str(respuesta_corta_b))
print("	La respuesta B es " + str(respuesta_b))
