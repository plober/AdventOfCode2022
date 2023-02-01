#!/usr/bin/env python3.10


largo = [line.rstrip() for line in open("input14.txt")]

corto = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".splitlines()

# The sand is pouring into the cave from point 500,0


class RegolithReservoir:

    def __init__(self, piedras: list[str]):

        self.resultado = []
        self.resultado: list[list[tuple[int,int]]]
        # [
        #  [(498, 4), (498, 6), (496, 6)],
        #  [(503, 4), (502, 4), (502, 9), (494, 9)]
        # ]
        equises, y_griegases = [], []
        for carrera in piedras:
            # "498,4 -> 498,6 -> 496,6"
            cadena = []
            for coordenadas in carrera.split(" -> "):
                # "496,6"
                [equis, y_griega] = coordenadas.split(',')
                y_griegases += [int(y_griega)]
                equises += [int(equis)]
                cadena.append((int(equis), int(y_griega)))
                # [(503, 4), (502, 4), (502, 9), (494, 9)]
            self.resultado.append(cadena)
        self.fuente = (0, 500)
        print(f"Fuente de arena en {self.fuente}")
        print(f"X varía entre {min(equises)} y {max(equises)}")
        print(f"Y varía entre {min(y_griegases)} y {max(y_griegases)}")

        self.mapa_en_blanco(max(y_griegases)+2, max(equises)-min(equises)+3)
        self.offset = (0, min(equises)-1)

        print(f"Offset de {self.offset}")

    def mirar_cadenas(self):
        """Muestra los datos de input, quedando como listas de listas de tuplas de coordenadas:
        resultado: list[list[tuple[int, int]]]"""
        for renglon in self.resultado:
            print(renglon)

    def mapa_en_blanco(self, alto: int = 70, ancho: int = 70, vidente = False):
        """Crea un mapa en blanco"""
        # En los datos, los X (ancho) varían entre 490 y 560 (Spread de 70)
        # En los datos, los Y (alto) varían entre 15 y 160 (spread de 155)
        if vidente: print(f"Mapa de {alto} por {ancho}")
        self.mapa = [["." for _ in range(ancho)] for _ in range(alto)]

    def agregar_fuente(self):
        """Agrega la fuente '+' en el mapa; idealmente en (0, 500)"""
        (x, y) = self.fuente
        self.poner_en_mapa(x, y, "+")

    def poner_en_mapa(self, posicion_vertical: int, posicion_horizontal: int, signo="#", vidente=False):
        """Recibe dos enteros y asigna al mapa un símbolo en esa coordenada"""
        if vidente:print(f" Agregando punto particular en x: {posicion_vertical - self.offset[0]} y: {posicion_horizontal - self.offset[1]}")
        self.mapa[posicion_vertical - self.offset[0]
                  ][posicion_horizontal - self.offset[1]] = signo

    def coordenada_en_mapa(self, coordenada, signo="#", vidente=False):
        """Recibe una coordenada y asigna al mapa un símbolo en esa coordenada"""
        self.poner_en_mapa(coordenada[0], coordenada[1], signo)

    def imprimir_mapa(self):
        """Presenta al mapa en su estado actual"""
        (x, y) = self.offset
        texto = f"({x},{y})"
        print(texto)
        for renglon in self.mapa:
            print(" " * len(texto)+"".join(renglon))
        #  {:<5s}
        print("{}^({},{})".format(
            " "*(len(self.mapa[0])-1+len(texto)), x+len(self.mapa[0]), y+len(self.mapa)))

    def agregar_swath(self, inicio: tuple[int, int], fin: tuple[int, int], vidente=False):
        """Agrega una fila o columna de piedras entre las coordenadas de Inicio y de Fin"""
        x_min, x_max = sorted([inicio[0], fin[0]+1]) # Estúpido range() X-D
        y_min, y_max = sorted([inicio[1], fin[1]+1]) # Estúpido range() X-D

        self.poner_en_mapa(inicio[1], inicio[0], "#")
        self.poner_en_mapa(fin[1], fin[0], "#")
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                if vidente: print(f" Agregando punto general en y: {y} x: {x}")
                self.poner_en_mapa(y, x, "#")

    def cargar_caminos(self, vidente = False):
        """Itera por el input, cargando cada uno de las paredes de piedra"""
        # [
        #  [(498, 4), (498, 6), (496, 6)],
        #  [(503, 4), (502, 4), (502, 9), (494, 9)]
        # ]
        for troncha in self.resultado:
            #  [(498, 4), (498, 6), (496, 6)]
            for i in range(len(troncha)-1):
                if vidente: print(f"Agregando camino {(troncha[i], troncha[i+1])}")
                self.agregar_swath(troncha[i], troncha[i+1])

    def caracter_en_mapa(self, coordenada: tuple[int,int]| list[int])-> str:
        """Devuelve el caracter recibido en la coordenada provista"""
        return self.mapa[coordenada[0]][coordenada[1]]

    def pispear_siguiente_posicion(self, coordenada: list[int]|tuple[int,int], movimiento: tuple[int,int], vidente = False)-> str:
        """Recibe una coordenada y un movimiento, verifica si el grano puede descender"""

        pispeo = (coordenada[0] + movimiento[0] - self.offset[0]), (coordenada[1]+movimiento[1]- self.offset[1])

        if vidente: print(locals())
        if vidente: print(f"Mapa de {len(self.mapa)} de alto por {len(self.mapa[0])} de ancho")
        
        if pispeo[1] < 0: return "X"                    # cae por izquierda del mapa, fin
        if pispeo[1] > len(self.mapa[0]): return "X"    # cae por derecha del mapa, fin
        if pispeo[0] >= len(self.mapa): return "X"      # cae por abajo, fin

        return self.mapa[pispeo[0]][pispeo[1]]

    def posicion_final(self, posicion_inicial: tuple[int,int], vidente = False) -> bool:
        siguiente_posicion = [posicion_inicial[0], posicion_inicial[1]]

        puede_caer = True
        habilitados = ".+/|\\"
        while puede_caer:
            # self.coordenada_en_mapa(siguiente_posicion, "X")
            if vidente: self.imprimir_mapa()

            if siguiente_posicion[0]+1 == len(self.mapa):
                print("Llegamos a un acuerdo")
                return False
            elif self.pispear_siguiente_posicion(siguiente_posicion,(1,0)) in habilitados: # Cae para abajo
                self.coordenada_en_mapa(siguiente_posicion, "|")
                siguiente_posicion[0] += 1
            elif self.pispear_siguiente_posicion(siguiente_posicion,(1,-1)) in habilitados: # Cae para un costado
                self.coordenada_en_mapa(siguiente_posicion, "/")
                siguiente_posicion[0] += 1
                siguiente_posicion[1] -= 1
            elif self.pispear_siguiente_posicion(siguiente_posicion,(1,1)) in habilitados: # Cae pal otro lado
                self.coordenada_en_mapa(siguiente_posicion, "\\")
                siguiente_posicion[0] += 1
                siguiente_posicion[1] += 1
            else: 
                self.coordenada_en_mapa(siguiente_posicion, "o")
                puede_caer = False
        
        if vidente: self.imprimir_mapa()

        return True
    
    def respuesta_a(self):
        self.agregar_fuente()
        self.cargar_caminos()
        # for _ in range(25): rta_corta.posicion_final((0,500))
        queda_espacio = True
        while queda_espacio:
           queda_espacio = self.posicion_final((0,500))
        respuesta_a = 0
        for renglon in self.mapa:
            respuesta_a += renglon.count("o")
        print(f"Respuesta A: {respuesta_a}")
        return respuesta_a
        

print("-"*5)
# rta_corta = RegolithReservoir(corto)
# rta_corta.respuesta_a()
# print(f"Tamaño de mapa = ({len(rta_corta.mapa)}, {len(rta_corta.mapa[0])})")
# print(f"Maximo de Zona = ({len(rta_corta.mapa[0])+rta_corta.offset[0]}, {len(rta_corta.mapa)+ rta_corta.offset[1]})")
# rta_corta.imprimir_mapa()

rta_larga = RegolithReservoir(largo)

rta_larga.agregar_fuente()
rta_larga.cargar_caminos()

rta_larga.imprimir_mapa()


RespuestaA, RespuestaB = rta_larga.respuesta_a(), 'N/A'
rta_larga.imprimir_mapa()


print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
