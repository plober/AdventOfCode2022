#!/usr/bin/env python3.10

largo = [line.rstrip() for line in open("input09.txt")]

# largo.pop()

corto = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".splitlines()

mapa_corto = """\
..##..
...##.
.####.
....#.
s###..\
""".split('\n')


class RopeBridge:

    def __init__(self, instrucciones):
        """Inicializando variables; consume un areglo como corto = ["R 4", "U 4", "L 3", "D 1"]"""
        self.instrucciones = instrucciones
        self.camino_cabeza = [(0, 0),]
        self.camino_cola = [(0, 0),]
        # Posiciones [0] es arriba/abajo y [1] es derecha/izq
        self.iniciar_diccionarios()
        self.posicion_relativa()
        self.mover_vibora()
        # ['NO', 'N',    'NE',
        #   'O', "Encima", 'E',
        #   'SO', 'S',    'SE',]

    def iniciar_diccionarios(self):
        self.rosa_de_los_vientos = ['N', 'NE', 'E', "SE", 'S', 'SO', 'O', "NO"]
        self.direccion_diccionario = {
            "U": (1, 0), "D": (-1, 0), "L": (0, -1), "R": (0, 1)}
        self.avanza_directo = {("N", "U"), ("S", "D"), ("E", "R"), ("O", "L")}
        self.cabeza_cabeza_horaria = {'N': 'NO', 'NE': 'N', 'E': 'NE', 'SE': 'E',
                                      'S': 'SE', 'SO': 'S', 'O': 'SO', 'NO': 'O'}
        self.cabeza_cabeza_antihoraria = {'NO': 'N', 'N': 'NE', 'NE': 'E', 'E': 'SE',
                                          'SE': 'S', 'S': 'SO', 'SO': 'O', 'O': 'NO'}
        self.giros_antihorarios = {("N", "L"), ("O", "D"), ("S", "R"), ("E", "U"),
                                   ("NO", "D"), ("SO", "R"), ("SE", "U"), ("NE", "L")}
        self.giros_horarios = {("N",  "R"), ("O",  "U"), ("S",  "L"), ("E",  "D"),
                               ("NE", "D"), ("SE", "L"), ("SO", "U"), ("NO", "R")}
        self.posiciones_orientadas = {(0,  0): "Encima",
                                      (1,  0): "N",
                                      (1,  1): "NE",
                                      (0,  1): "E",
                                      (-1,  1): "SE",
                                      (-1,  0): "S",
                                      (-1, -1): "SO",
                                      (0, -1): "O",
                                      (1, -1): "NO"
                                      }

    def posicion_relativa(self):
        """Posición relativa es ['N', 'NE', 'E', "SE", 'S', 'SO', 'O', "NO", "Encima"] o "Muy lejos"""
        diferencia_posiciones = (self.camino_cabeza[-1][0] - self.camino_cola[-1][0],
                                 self.camino_cabeza[-1][1] - self.camino_cola[-1][1])
        return self.posiciones_orientadas.get(diferencia_posiciones, "Muy Lejos")

    def armar_mapa(self, alto, ancho, offset=(0, 0)):
        armando = ["." * (ancho + offset[1] + 1)] * (alto + offset[0] + 1)
        armando[-1-offset[0]] = ("." * offset[1] + "s"+"."*(ancho-1-offset[1]))
        return armando

    def visualizar_mapa(self, camino, caracter="#"):
        offset = (abs(min(i[0] for i in camino)),
                  abs(min(i[1] for i in camino)))
        mapita = self.armar_mapa(max(i[0] for i in camino) + offset[0],
                                 max(i[1] for i in camino) + offset[1])

        print("Visualizar Mapa para {}".format(camino))
        for lugar in camino[1:]:
            mapita[-1-lugar[0]+offset[0]] = mapita[-1-lugar[0]+offset[0]][:lugar[1]+offset[1]] + \
                caracter +  \
                mapita[-1-lugar[0]+offset[0]][1+lugar[1]+offset[1]:]
        for regla in mapita:
            print("".join(regla))

    def visualizar_cabeza(self):
        self.visualizar_mapa(self.camino_cabeza, "@")

    def visualizar_cola(self):
        self.visualizar_mapa(self.camino_cola, "#")
# Recorrido Cola
# ..##..
# ...##.
# .####.
# ....#.
# s###..

    def mover_vibora(self, vidente = False):
        if vidente: print("Posición Inicial: {}".format(self.camino_cola[-1]))
        for instruccion in self.instrucciones:

            direccion, avanza = self.direccion_diccionario[instruccion[0]], int(
                instruccion[2:])
            # self.posicion_cabeza

            for _ in range(1, min(3, avanza+1)):
                self.camino_cabeza.append((self.camino_cabeza[-1][0] + direccion[0],
                                           self.camino_cabeza[-1][1] + direccion[1]))
                posicion_relativa = self.posicion_relativa()
                if posicion_relativa == "Muy Lejos":
                    self.camino_cola.append(self.camino_cabeza[-2])

            for _ in range(3, 1 + avanza):
                self.camino_cola.append(self.camino_cabeza[-1])
                self.camino_cabeza.append((self.camino_cabeza[-1][0] + direccion[0],
                                           self.camino_cabeza[-1][1] + direccion[1]))
            if vidente: print("Instrucción: {}; posición: {}".format(
                instruccion, self.camino_cola[-1]))

    def conteo_pasos_registrados_propio(self):
        return self.conteo_pasos_registrados(self.camino_cola)

    def conteo_pasos_registrados(self, recorrido):
        return len(set(recorrido))


rta_corta = RopeBridge(corto)
# print(rta_corta.camino_cabeza)
assert rta_corta.conteo_pasos_registrados_propio() == 13


rta_larga=RopeBridge(largo)
RespuestaA, RespuestaB = rta_larga.conteo_pasos_registrados_propio(), 'N/A'


print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
