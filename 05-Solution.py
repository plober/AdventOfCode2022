#!/usr/bin/env python3.10


lines, largo=[], []
with open("input05.txt") as file_object:
  lines = file_object.readlines()

for line in lines:
  largo.append(line.rstrip())


cortoTexto="""    [D]
[N] [C]
[Z] [M] [P]
 1   2   3 """

cortoInicial =[]
for line in cortoTexto.split('\n'):
   cortoInicial.append(line)

cortoMovimientos=[  "move 1 from 2 to 1",
                    "move 3 from 1 to 3",
                    "move 2 from 2 to 1",
                    "move 1 from 1 to 2"]
# Stacks Página 615

class CalcularA:

    def parseoSituacion(Situacion):
        #[x for x in beta if x not in "[]"][::2]
        Situacion.reverse()
        renglones = len (Situacion)
        largo = len (Situacion[0])
        DiccionarioPilas = dict={}

        for caracterColumna in range(len(Situacion[0]))[1::4]:
            Traspuesto = ['{: <{}}'.format(fila,largo)[caracterColumna] for fila in Situacion]
            DiccionarioPilas[int(Traspuesto[0])] = ''.join(Traspuesto[1:]).strip()
        return DiccionarioPilas

    def parseoMovimientos(Movimientos):
        Actividad=[]
        for linea in Movimientos:
            [trash, uno, trash, dos, trash, tres] = linea.split()
            Actividad.append([int(uno), int(dos), int(tres)])
        return Actividad


    def solucionar(SituacionInicial, Movimientos):
        pass


RespuestaCortaA, RespuestaA, RespuestaCortaB, RespuestaB = 'N/A', 'N/A', 'N/A', 'N/A'

assert CalcularA.parseoSituacion(cortoInicial)=={1:"ZN",2:"MCD", 3:"P"}
assert CalcularA.parseoMovimientos(cortoMovimientos)==[[1,2,1],[3,1,3],[2,2,1],[1,1,2]]
#assert CalcularA.solucionar(cortoInicial,cortoMovimientos)=="CMZ"
print("	La respuesta del Ejemplo A es " + str(RespuestaCortaA))
print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta del Ejemplo B es " + str(RespuestaCortaB))
print("	La respuesta B es " + str(RespuestaB))
