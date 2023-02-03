#!/usr/bin/env python3.10
import matplotlib.pyplot as plt

largo = [line.rstrip() for line in open("input15.txt")]
corto = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".splitlines()


class BeaconExclusionZone:

    def __init__(self, plano_crudo: list[str]):

        self.sensores_a_faro: dict[tuple[int, int], tuple[int, int]]
        self.sensores_a_faro = dict()
        # {(13, 2) : (15, 3)}
        self.sensores_radio: dict[tuple[int, int], int]
        self.sensores_radio = dict()
        # {(13, 2) : 3}

        for line in plano_crudo:
            # Sensor at x=12, y=14: closest beacon is at x=10, y=16
            usable = "".join(
                [letra for letra in line if letra in "0123456789,:-"]).replace(":", ",").split(",")
            self.sensores_a_faro[(int(usable[0]), int(usable[1]))] = (
                int(usable[2]), int(usable[3]))

        max_offset = 0

        for key in self.sensores_a_faro:
            self.sensores_radio[key] = abs(
                key[0] - self.sensores_a_faro[key][0]) + abs(key[1] - self.sensores_a_faro[key][1])
            max_offset = min(max_offset, key[0] - self.sensores_radio[key])

        self.max_offset = 0

    def sombra_en_linea(self, sensor: tuple[int, int], renglon: int, vidente=False) -> tuple[int, int]:
        """Recibe una coordenada de Sensor y el renglón y devuelve la tupla de rango del área donde sé que no puede haber.
        Nota: si el comienzo y fin del rango tienen el mismo valor (tipo range(13,13), es que no hay exclusion)"""
        distancia_al_renglon = abs(sensor[1] - renglon)
        # Sensor at x=8, y=7: closest beacon is at x=2, y=10
        quequeda = max(self.sensores_radio[sensor] - distancia_al_renglon, -1)
        if vidente:
            print("-"*3)
            print(
                f"Verificando : {sensor}, radio {self.sensores_radio[sensor]}")
            print(f"   Renglon: {renglon}")
            print(f"    Distancia al renglon: {distancia_al_renglon}")
            print(f"    Posicion y: {sensor[1]}")
            print(f"    Lo que queda: {quequeda}")
            print(
                f" Sombra en linea: {None if quequeda==0 else (sensor[0] - quequeda, sensor[0] + quequeda+1)}")
        # distancia al renglon = 3
        # if quequeda == 0: return None
        return (sensor[0] - quequeda, sensor[0] + quequeda+1)

    def sombras_en_la_linea(self, renglon: int, vidente=False) -> list[tuple[int, int]]:
        """Cicla por todos los sensores, registrando si excluye alguna parte del renglón destino"""
        # Ojo que hay sombras en x negativos
        candidatos = []
        for sensor in self.sensores_a_faro:
            if vidente:
                print(
                    f"Verificando : {sensor}, radio {self.sensores_radio[sensor]}")
            candidatos.append(self.sombra_en_linea(sensor, renglon))
        intervalos_sin_faros = [
            intervalo for intervalo in candidatos if intervalo[0] < intervalo[1]]
        return intervalos_sin_faros

    def muestra_renglon(self, sensor: tuple[int, int], renglon: int, con_offset=False) -> str:
        linea: list[str]
        linea = ["."] * (self.sensores_radio[sensor] + 1) + \
            ["s"] + ["."] * (self.sensores_radio[sensor] + 1)
        sombras = self.sombra_en_linea(sensor, renglon, vidente=False)
        offset_x = self.sensores_radio[sensor] - sensor[0] + 1
        # offset_x = self.max_offset
        if con_offset:
            linea.insert(
                0, " " * (sensor[0] - self.sensores_radio[sensor] + self.max_offset))
        if offset_x < 0:
            return "".join(linea)
        linea[offset_x] = "|"
        linea[self.sensores_radio[sensor] + 1] = "s"

        for i in range(sombras[0] + offset_x, sombras[1] + offset_x):
            linea[i] = "#"  # this the magic

        if sensor[1] == renglon:
            linea[self.sensores_radio[sensor] + 1] = "S"

        return "".join(linea)

    def respuesta_a(self, renglon: int, vidente=False) -> int:
        intervalos_vacios = self.sombras_en_la_linea(renglon)
        # [(12, 13), (2, 15), (2, 3), (-2, 3), (16, 25), (14, 19)]
        intervalos_vacios.sort()
        # [(-2, 3), (2, 3), (2, 15), (12, 13), (14, 19), (16, 25)]

        sombra_total = [intervalos_vacios[0]]
        # [(-2, 3)]

        for (inicio, fin) in intervalos_vacios:
            # Tres casos:
            #   a) Que el intervalo esté en contenido la Sombra Total
            #   b) Que el intervalo se superponga y haya que extender a Sombra Total
            #   c) Que el intervalo no superponga
            # : Tener en cuenta que están ordenados por su primer elemento

            if fin <= sombra_total[-1][1]:
                pass  # a) está contenido
            elif sombra_total[-1][0] <= inicio <= sombra_total[-1][1] <= fin:  # b Se superpone
                sombra_total[-1] = (sombra_total[-1][0], fin)
            elif sombra_total[-1][1] < inicio:  # c) está aparte
                sombra_total.append((inicio, fin))

        respuesta_a = self.conteo_vacios(sombra_total)

        set_faros_en_renglon = set()

        for key in self.sensores_a_faro:
            if self.sensores_a_faro[key][1] == renglon:
                set_faros_en_renglon.add(self.sensores_a_faro[key])
                if vidente:
                    print(f"{key}: {self.sensores_a_faro[key]}")
        respuesta_a -= len(set_faros_en_renglon)

        return respuesta_a

    def conteo_vacios(self, intervalos_vacios: list[tuple[int, int]]) -> int:
        cantidad_vacios = 0
        for (inicio, fin) in intervalos_vacios:
            cantidad_vacios += fin - inicio
        return cantidad_vacios

    def matriz_gaps(self, vidente=False) -> dict:
        """Tira las tachodistancias entre cada par de sensores restándole los radios correspondientes.
        Eso me daría una cadena de coordenadas bastante limitada de gaps de 1 que revisar."""
        interesantes = dict()

        for origen in self.sensores_radio:
            for destino in self.sensores_radio:
                gap = (abs(origen[0] - destino[0])
                       + abs(origen[1] - destino[1])
                       - self.sensores_radio[origen]
                       - self.sensores_radio[destino]
                       - 1)
                if gap == 1:
                    if vidente:
                        print(
                            f"\tEntre {origen} y {destino} hay una brecha de {gap}")
                    if destino not in interesantes:  # Acá ya me estoy haciendo el vivo, y funciona
                        interesantes[origen] = destino
        return interesantes

    def identificar_solucion(self, diccionario_de_dos: dict[tuple[int, int], tuple[int, int]], vidente=False) -> tuple[int, int]:
        # Resolver una ecuación lineal de intersección de dos rectas que pasan por números enteros y tienen 1 de pendiente.
        def por_h_por_b(izquierda, derecha) -> tuple[int, int]:
            """Devuelve ordenada al origen y signo de pendiente"""
            # Lo podría haber hecho más corto y críptico tomando el extremo derecho de la coordenada izquierda
            [izquierda, derecha] = sorted([izquierda, derecha])  # Just in case
            x_izquierda, y_izquierda = izquierda
            x_derecha, y_derecha = derecha
            if y_izquierda > y_derecha:  # la pendiente es positiva
                pendiente = 1
                punto_mas_bajo = y_izquierda - self.sensores_radio[izquierda]
                ordenada_al_origen = punto_mas_bajo - x_izquierda
            elif y_izquierda < y_derecha:  # la pendiente es negativa
                pendiente = -1
                punto_mas_alto = y_izquierda + self.sensores_radio[izquierda]
                ordenada_al_origen = punto_mas_alto + x_izquierda
            else:
                # si están a la misma altura, no determinan un punto y realmente no me sirven.
                return TypeError
            return (pendiente, ordenada_al_origen)

        sensor_1, sensor_2 = sorted(diccionario_de_dos.popitem())
        if vidente:
            print(f"{(sensor_1, sensor_2)} Sensores 1 y 2")
        (a, b) = por_h_por_b(sensor_1, sensor_2)
        if vidente:
            print(f"{(a,b)} pendiente y ordenada al origen")
        # [numero // 21000 for numero in [3164509, 3196584, 3740685, 2657814, 3750994, 3221696, 3190979, 2626436]]
        sensor_3, sensor_4 = sorted(diccionario_de_dos.popitem())
        if vidente:
            print(f"\t{(sensor_3, sensor_4)} Sensores 3 y 4")
        (c, d) = por_h_por_b(sensor_3, sensor_4)
        if vidente:
            print(f"\t{(c,d)} pendiente y ordenada al origen")
        # Solucionar ecucacion lineal
        (_, ordenada_al_origen_pendiente_negativa), (_,
                                                     ordenada_al_origen_pendiente_positiva) = sorted([(a, b), (c, d)])
        posicion_x = (ordenada_al_origen_pendiente_negativa -
                      ordenada_al_origen_pendiente_positiva)//2+1
        posicion_y = ordenada_al_origen_pendiente_positiva + posicion_x-1 #jodeme que le erraba por uno DDDDD-X

        return (posicion_x, posicion_y)

    def respuesta_b(self) -> int:
        interesantes = self.matriz_gaps()

        print(f"Interesantes: {interesantes}")
        for key in interesantes:
            print(f"{key} tiene radio de {self.sensores_radio[key]}")
            print(
                f"{interesantes[key]} tiene radio de {self.sensores_radio[interesantes[key]]}")

        (x, y) = self.identificar_solucion(interesantes)
        print(f"Hueco encontrado en {(x, y)}")
        return (x * 4000000 + y)

    def tachodistancia(self, desde: tuple[int, int], hasta: tuple[int, int]) -> int:
        """Calcula la distancia de taxi"""
        x_desde, y_desde = desde
        x_hasta, y_hasta = hasta
        return abs(x_desde - x_hasta) + abs(y_desde - y_hasta)

    def graficar(self, factor = 1.0):
        plt.axis
        plt.title("Grafico de Sensores y Faros")
        max = 4_000_000
        posicion_x = [0,max,max,0,0]
        posicion_y = [0,0,max,max,0]
        plt.plot(posicion_x, posicion_y, label = f"Marco")

        for (x, y) in self.sensores_radio:
            faro_x, faro_y = self.sensores_a_faro[(x,y)]
            radio = self.sensores_radio[(x, y)]/factor
            posicion_x = [x - radio , x         , x + radio , x         , x - radio ]
            posicion_y = [y         , y + radio , y         , y - radio , y         ]
            plt.plot(posicion_x, posicion_y, label = f"{(x, y)}", 
                color="b" if x in {3164509, 3196584, 3740685, 2657814, 3750994, 3221696, 3190979, 2626436} else "grey")
            plt.plot(x, y, marker="o", color="b" if x in {3164509, 3196584, 3740685, 2657814, 3750994, 3221696, 3190979, 2626436} else "grey")
            plt.plot([x, faro_x], [y, faro_y], color = "gray")
            plt.plot(faro_x, faro_y, marker="*", color="r")
        # plt.legend()
        
        plt.show()



rta_corta = BeaconExclusionZone(corto)

if False:
    print(rta_corta.muestra_renglon((8,  7), 7))
    print(rta_corta.muestra_renglon((8,  7), 10))
    print(rta_corta.muestra_renglon((8,  7), 16))
    print(rta_corta.muestra_renglon((8,  7), 17))

assert rta_corta.sensores_a_faro[(2, 18)] == (-2, 15)
assert rta_corta.sensores_a_faro[(14, 17)] == (10, 16)
assert rta_corta.sensores_radio[(2, 18)] == 7
assert rta_corta.sensores_radio[(14, 17)] == 5

# Sensor at x=8, y=7: closest beacon is at x=2, y=10
assert rta_corta.sombra_en_linea((8, 7), 10, vidente=False) == (2, 15)
assert rta_corta.respuesta_a(10) == 26

print(f"Respuesta corta A: {rta_corta.respuesta_a(10)}")

rta_corta.matriz_gaps()
# rta_corta.graficar()


# print("Sensores_radio " + "-" * 5)
# for key in rta_corta.sensores_a_faro:
#     print(f"   {key}:\t distancia {rta_corta.sensores_radio[key]} a {rta_corta.sensores_a_faro[key]}")

# print("Sombra_en_linea" + "-" * 5)
# for key in rta_corta.sensores_a_faro:
#     print(f"   {key}:\t intervalo linea {rta_corta.sombra_en_linea(key, 10)}")

# print("Muestra_renglon " + "-" * 5)
# for key in rta_corta.sensores_a_faro:
#     print(f"   {key}:\t sombra linea {rta_corta.muestra_renglon(key, 10, con_offset=True)}")
rta_larga = BeaconExclusionZone(largo)
# rta_larga.graficar()

RespuestaA, RespuestaB = rta_larga.respuesta_a(
    2000000), rta_larga.respuesta_b()

assert RespuestaB == 13639962836448, f"Le estás errando por {RespuestaB - 13639962836448}"


print("	La respuesta A es " + str(RespuestaA))
print("	  That's not the right answer; your answer is too low. (You guessed 4000000.)")
print("	La respuesta B es " + str(RespuestaB))
print("	  That's not the right answer; your answer is too low. (You guessed 13639958836448.)")
print("	  That's not the right answer; your answer is too low. (You guessed 13639962836449.)")
