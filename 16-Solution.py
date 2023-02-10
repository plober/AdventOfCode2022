#!/usr/bin/env python3.10
import itertools

largo = [line.rstrip() for line in open("input16.txt")]
corto = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()

class ProboscideaVolcanium:

    # Entiendo que tengo que calcular las distancias desde AA hasta cada
    #  válvula con flowrate no cero; y entre esas válvulas para armar una grilla de distancias.
    # Luego voy explorando las secuencias de encendido de manera que T-[rate] maxeen.
    #  Sospecho que el Greedy de maxeo no es el mejor camino; pero es una buena idea buscarlo
    # para descartar alternativas apenas queden por debajo; e ir mejorando el benchmark para
    # no tener que explorar 15! ~= 1.3*10^12 alternativas.

    def __init__(self, input: list[str], vidente=False):
        flujos_de_valvulas = dict()
        flujos_de_valvulas: dict[str, int]
        destinos_posibles = dict()
        destinos_posibles: dict[str, list[str]]
        self.resultados: list[tuple[int, list[str]]]
        self.resultados = []
        for renglon in input:
            # "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
            _, valvula, _, _, rate, * \
                _, caminos = renglon.split(maxsplit=9)  # Heck yea!
            flujos_de_valvulas[valvula] = int(rate.strip("rate=;"))
            destinos_posibles[valvula] = caminos.split(", ")
        self.importantes = {
            valvula for valvula in flujos_de_valvulas if flujos_de_valvulas[valvula] > 0}
        # self.importantes.add("AA") # Porque empieza acá y necesito las distancias
        if vidente:
            print(f"Válvulas de flujo no nulo: {self.importantes}")
            for valvula in flujos_de_valvulas:
                print(
                    f"{'>' if flujos_de_valvulas[valvula] > 0 else ' '}{valvula}: flujo {flujos_de_valvulas[valvula]}; destinos: {destinos_posibles[valvula]}")
        self.flujos_por_valvula: dict[str, int]
        self.flujos_por_valvula = flujos_de_valvulas
        # {"AA": 0}
        self.destinos_posibles: dict[str, list[str]]
        self.destinos_posibles = destinos_posibles
        # {AA: [DD, II, BB]}
        pass

    def despresurizacion_por_apertura(self, lista_valvulas: list[str], minutos_disponibles=30, valvula="AA", vidente=False) -> int:
        """Devuelve la despresurización total generada por un recorrido que solo menciona las válvulas que se van abriendo"""
        if vidente: print(f"Recorrido: {lista_valvulas}")
        minuto_de_este_paso = 0
        despresurizacion_final = 0
        despresurizacion_por_minuto = 0
        for mirando_valvula in lista_valvulas:
            minuto_de_este_paso += self.diccionario_distancias[valvula][mirando_valvula]+1
            if minutos_disponibles - minuto_de_este_paso < 0: break
            valvula = mirando_valvula
            despresurizacion_final += self.flujos_por_valvula[valvula] * (minutos_disponibles - minuto_de_este_paso)
            despresurizacion_por_minuto += self.flujos_por_valvula[valvula]
            if vidente:print(f"Minuto {minuto_de_este_paso} - abre {valvula}, para descomprimir {despresurizacion_por_minuto} por minuto")
        return despresurizacion_final

    def crear_diccionario_de_distancias(self, vidente=False):
        """Genera el diccionario de distancias entre válvulas con flujos no cero"""
        diccionario_distancias = dict()
        diccionario_distancias: dict[str, dict[str, int]]
        if vidente:
            print("\nCreando diccionario de distancias.")
            print(f"Empiezo por el principio: AA")
        diccionario_distancias["AA"] = self.calculo_distancias("AA")
        # diccionario_distancias["AA"]["BB"]: 6

        for valvula in self.importantes:
            if vidente:
                print(f"\nUno de los importantes: {valvula}")
            diccionario_distancias[valvula] = self.calculo_distancias(valvula)
        if vidente:
            for origen in diccionario_distancias:
                print(f"\t Desde {origen}")

                for destino in diccionario_distancias[origen]:
                    print(
                        f"\t\t a {destino} hay {diccionario_distancias[origen][destino]} de distancia")
        self.diccionario_distancias = diccionario_distancias

    def calculo_distancias(self, origen: str, vidente=False) -> dict[str, int]:
        """Calcula distancias desde el parámetro provisto hasta cada uno de las 
        válvulas con flujo mayor a cero, devolviendo un diccionario"""

        diccionario_caminos = dict()
        diccionario_caminos: dict[str, int]
        revisados = {origen}
        revisar = {
            mirar for mirar in self.destinos_posibles[origen]} - {origen}
        if vidente:
            print(f"Importantes: {self.importantes}")
            print(f" Trabajando con: {origen}")
        distancia = 0
        while not self.importantes <= revisados:
            # Mientras haya alguno importante que no haya sido revisado
            distancia += 1
            if vidente:
                print(f"Distancia {distancia}, revisar: {revisar}")
            revisar_despues = set()
            revisar_despues: set[str]
            for foco in revisar.difference(revisados):
                # itera por cada destino que no haya sido revisado
                # Agrego los destinos que vengan después del Foco
                revisar_despues.update(self.destinos_posibles[foco])
                if vidente:print(f"  Chequeo '{origen}'->'{foco}'", end="")
                if foco in self.importantes:
                    diccionario_caminos[foco] = distancia
                    # Para que quede diccionario_distancias[origen][foco] = distancia
                    if vidente:print(f" {distancia} de distancia")
                else: 
                    if vidente:print(f" no importa")
            revisados.update(revisar)
            # Carga todos los destinos accesibles para el siguiente paso
            revisar = revisar_despues - {origen}

            if vidente:
                print(f" Revisados: {revisados}\n")
            limite = 1000
            if distancia >= limite:
                print(f"{limite} de distancia alcanzado, hubo un error")
                for key in diccionario_caminos:
                    print(origen, "->", key, diccionario_caminos[key])
                return diccionario_caminos
        if vidente:
            print(
                f"Todos los importantes fueron agregados y medidos: {self.importantes <= revisados}")
        return diccionario_caminos

    def calcular_caudal_por_camino(self, camino: list[str], valvula="AA", minutos_disponibles=30, vidente=False) -> int:
        """Devuelve la despresurización total que aporta el camino provisto"""
        if vidente: print(f"Recorrido a evaluar: {camino}")
        minuto_actual = 0
        despresurizacion_final = 0
        despresurizacion_por_minuto = 0
        for paso in camino:
            minuto_actual += self.diccionario_distancias[valvula][paso]+1
            valvula = paso
            despresurizacion_final += self.flujos_por_valvula[valvula] * (minutos_disponibles - minuto_actual)
            despresurizacion_por_minuto += self.flujos_por_valvula[valvula]
            if vidente:print(f" Evaluando abrir {valvula} al minuto {minuto_actual} para descomprimir {despresurizacion_por_minuto} por minuto")
        return despresurizacion_final

    def mostrar_sistema_de_cavernas(self):
        """Muestra las distancias entre las válvulas, y el caudal que esa válvula ofrece en las intersecciones correspondientes"""
        indices = sorted(list(self.importantes))

        print("\n ", end="")
        for origen in indices:
            print(" {: <5}".format(origen), end="")
        print("")
        for origen in ["AA"]+indices:
            for destino in indices:
                if origen == destino:print(f"({(self.flujos_por_valvula[origen]): >3}) ", end="")
                else:print("{: >4}  ".format(self.diccionario_distancias[origen][destino]), end="")
            print("  {}".format(origen))
        print("")

    def calcular_demoras(self, camino: list[str]) -> int:
        """Devuelve el tiempo necesario para pasar abrir a todas las válvulas mencionadas, en orden"""
        return sum(self.diccionario_distancias[desde][hasta]+1 for desde, hasta in itertools.pairwise(camino))

    def camino_de_respuesta_profundidad_1(self, minutos_disponibles=30, vidente=False) -> list[str]:
        """Devuelve el camino con respuesta más greedy"""
        mejor_camino = ["AA"]
        valvulas_sin_usar = self.importantes.copy()
        candidato: tuple[int,str]
        opciones: list[tuple[int,str]]
        if vidente: print(f"Midiendo Camino de Respuesta Profundidad 1")
        while minutos_disponibles >= 0 and len(valvulas_sin_usar) >= 1:
            # qué pasas si quedan 

            opciones = [(0 , "AA")]
            for valvula in valvulas_sin_usar:
                minutos_restantes = minutos_disponibles - self.diccionario_distancias[opciones[-1][1]][valvula] 
                if minutos_restantes >= 0:
                    candidato = (minutos_restantes * self.flujos_por_valvula[valvula], valvula)
                    opciones.append(candidato)
                    if vidente: print(f" Evaluando abrir {valvula} al minuto {minutos_disponibles} para descomprimir {minutos_restantes * self.flujos_por_valvula[valvula]} por minuto")
            mejor_candidato = sorted(opciones)[-1][1]
            mejor_camino.append(mejor_candidato)
            if vidente: print(f" Opciones disponibles: {sorted(opciones)}\n La mejor es {sorted(opciones)[-1]}")
            valvulas_sin_usar.remove(mejor_candidato)
        mejor_camino.remove("AA")
        return mejor_camino
        
    def camino_de_respuesta_profundidad_2(self, minutos_disponibles=30, vidente=False) -> list[str]:
        """Devuelve el camino con respuesta mirando uno más allá"""
        mejor_camino = ["AA"]
        valvulas_sin_usar = self.importantes.copy()
        candidato: tuple[int,str]
        opciones: list[tuple[int,str]]
        if vidente: print(f"Midiendo Camino de Respuesta Profundidad 2")
        while minutos_disponibles >= 0 and len(valvulas_sin_usar) >= 1:
            # qué pasas si quedan 
            opciones = [(0 , "AA")]
            for valvula_1, valvula_2 in itertools.permutations(valvulas_sin_usar,2):
                este_paso = self.diccionario_distancias[mejor_camino[-1]][valvula_1] -1
                siguiente_paso = self.diccionario_distancias[valvula_1][valvula_2] -1
                minutos_restantes = minutos_disponibles - este_paso

                if minutos_restantes >= 0:
                    candidato = (
                        minutos_restantes * self.flujos_por_valvula[valvula_1] + 
                        (minutos_restantes - siguiente_paso) * self.flujos_por_valvula[valvula_2]
                        , valvula_1)
                    opciones.append(candidato)
                    if vidente: print(f" Evaluando abrir {valvula_1} y {valvula_2} al minuto {minutos_disponibles} para descomprimir {candidato[0]} para cuando termine")
                    # if vidente: print("  dist({}-{}) = {}".format(mejor_camino[-1],valvula_1, este_paso))
                    # if vidente: print("  dist({}-{}) = {}".format(valvula_1, valvula_2, siguiente_paso))

            mejor_candidato = sorted(opciones)[-1][1]
            if mejor_candidato =="AA": 
                mejor_camino.append(valvulas_sin_usar.pop())
                break
            if len(valvulas_sin_usar) == 1 : mejor_candidato = valvulas_sin_usar.pop()
            minutos_disponibles -= self.diccionario_distancias[mejor_camino[-1]][mejor_candidato] + 1
            if vidente: print(f" Opciones disponibles: {sorted(opciones)}\n La mejor es {sorted(opciones)[-1]}")
            mejor_camino.append(mejor_candidato)
            valvulas_sin_usar.remove(mejor_candidato)
        mejor_camino.remove("AA")
        return mejor_camino

    def generador_de_todos_los_recorridos_validos(self, 
                                                  sin_usar: list[str]|None = None, 
                                                  cargando = [],
                                                  minutos_disponibles=30,
                                                  anterior ="AA", 
                                                  vidente=False):
        """Un generador de las permutaciones de válvula que sumen menos de 30' entre viajes y aperturas"""
        if sin_usar == None: sin_usar = list(self.importantes)
        tabulador = 10 - max(len(sin_usar),1)*2
        respuesta = []
        respuesta: list[str]
        if len(sin_usar) == 1: 
            respuesta = cargando + sin_usar
            self.resultados.append((self.despresurizacion_por_apertura(respuesta), respuesta))
            # print(" " * tabulador +f"Ultimo: ({self.despresurizacion_por_apertura(respuesta)}) {respuesta}")
        else: 
            for considerando in sin_usar:
                minutos_restantes = minutos_disponibles - self.diccionario_distancias[anterior][considerando]+1
                if minutos_restantes >= 0:
                    if vidente: print(" " * tabulador +f"Quedan {minutos_restantes}, pruebo con {considerando} de {sin_usar}")
                    carry = cargando + [considerando]
                    intento = self.generador_de_todos_los_recorridos_validos(list(set(sin_usar)-{considerando}), 
                                                                    carry,
                                                                    minutos_restantes, 
                                                                    considerando, 
                                                                    vidente) # type: ignore
                    if cargando == []: respuesta.append(intento)# type: ignore
                else: 
                    if vidente: print(" " * tabulador + f"No queda tiempo para {considerando}")
        return respuesta

    def generatriz(self, 
                    sin_usar: list[str]|None = None, 
                    cargando = [],
                    minutos_disponibles=30,
                    anterior ="AA", 
                    vidente=False):
        """Un generador de las permutaciones de válvula que sumen menos de 30' entre viajes y aperturas"""
        if sin_usar == None: sin_usar = list(self.importantes)
        tabulador = 10 - max(len(sin_usar),1)*2
        respuesta = []
        respuesta: list[str]
        if len(sin_usar) == 1: 
            respuesta = cargando + sin_usar
            self.resultados.append((self.despresurizacion_por_apertura(respuesta), respuesta))
            # print(" " * tabulador +f"Ultimo: ({self.despresurizacion_por_apertura(respuesta)}) {respuesta}")
        else: 
            for considerando in sin_usar:
                minutos_restantes = minutos_disponibles - self.diccionario_distancias[anterior][considerando]+1
                if minutos_restantes >= 0:
                    if vidente: print(" " * tabulador +f"Quedan {minutos_restantes}, pruebo con {considerando} de {sin_usar}")
                    carry = cargando + [considerando]
                    intento = self.generatriz(list(set(sin_usar)-{considerando}), 
                                                                    carry,
                                                                    minutos_restantes, 
                                                                    considerando, 
                                                                    vidente) # type: ignore
                    if cargando == []: respuesta.append(intento)# type: ignore
                else: 
                    self.resultados.append((self.despresurizacion_por_apertura(cargando), cargando))
                    if vidente: print(" " * tabulador + f"No queda tiempo para {considerando}")
        return respuesta

rta_corta = ProboscideaVolcanium(corto)
rta_corta.crear_diccionario_de_distancias()
rta_corta.mostrar_sistema_de_cavernas()

if False: # Pispear resultados del generador
    print("-"*10+"Generador"+"-"*10)
    ponele = rta_corta.generador_de_todos_los_recorridos_validos(vidente=False)
    print(f"Respuesta final (entre {len(rta_corta.resultados)}): ")
    rta_corta.resultados.sort()
    for i in rta_corta.resultados[:5] +["///"] +rta_corta.resultados[-5:]: print(i)
    print("/"*10+"Generador"+"/"*10)

if True: # Pispear resultados de Generatriz
    print("-"*10+"Generatriz"+"-"*10)
    ponele = rta_corta.generatriz(vidente=False)
    print(f"Respuesta final (entre {len(rta_corta.resultados)}): ")
    rta_corta.resultados.sort()
    for i in rta_corta.resultados[:5] +["///"] +rta_corta.resultados[-5:]: print(i)
    print("/"*10+"Generatriz"+"/"*10)
    print("")

miron = False
if miron: 
    print(f'Medicion tentativa: {rta_corta.comparar_caudal_por_camionmedir_camino(["DD", "BB", "JJ", "HH", "EE", "CC"], miron)}')
    print(f'Medicion tentativa: {rta_corta.comparar_caudal_por_camionmedir_camino(["DD", "BB", "JJ", "HH", "CC", "EE"], miron)}')
    print(f'Medicion tentativa: {rta_corta.comparar_caudal_por_camionmedir_camino(["DD", "JJ", "BB", "HH", "EE", "CC"], miron)}')
    print(f'Medicion tentativa: {rta_corta.comparar_caudal_por_camionmedir_camino(["DD", "EE", "BB", "JJ", "HH", "EE", "CC"], miron)}')
    print(f'Medicion tentativa: {rta_corta.comparar_caudal_por_camionmedir_camino(["EE", "DD", "BB", "JJ", "HH", "CC"], miron)}')
    print("-"*10)

medicion_rta_corta_a, valvulas_rta_corta_a = rta_corta.resultados[-1]

print(f"Valvulas Respuesta Corta: {valvulas_rta_corta_a}")
print(f"Medición respuesta corta: {medicion_rta_corta_a}")
assert valvulas_rta_corta_a == ["DD", "BB", "JJ", "HH", "EE", "CC"]
assert medicion_rta_corta_a == 1651, f"La despresurización medida es incorrecta, erró por {1651 - medicion_rta_corta_a}"
# ////////////////////////
if True: #buscar la rta larga A
    print("Comienzo cálculos Rta Larga")
    rta_larga = ProboscideaVolcanium(largo)
    rta_larga.crear_diccionario_de_distancias()
    rta_larga.mostrar_sistema_de_cavernas()

    respuesta_profunda_1 = rta_larga.camino_de_respuesta_profundidad_1()
    respuesta_profunda_2 = rta_larga.camino_de_respuesta_profundidad_2()

    rta_larga_caudal_1 = rta_larga.despresurizacion_por_apertura(respuesta_profunda_1)
    rta_larga_caudal_2 = rta_larga.despresurizacion_por_apertura(respuesta_profunda_2)

    print("Respuesta profunda 1: {}, {}".format(rta_larga_caudal_1, respuesta_profunda_1))
    print("Respuesta profunda 2: {}, {}".format(rta_larga_caudal_2, respuesta_profunda_2))



    if False: # Pispear resultados por generador
        rta_larga.generador_de_todos_los_recorridos_validos()
        rta_larga.resultados.sort()
        print("-"*10+"Generador"+"-"*10)
        print(f"Respuesta final larga (entre {len(rta_larga.resultados)}): ")    
        for i in rta_larga.resultados[:5] +["///"] +rta_larga.resultados[-5:]: print(i)
        print("/"*10+"Generador"+"/"*10)

        medicion_rta_larga_a, valvulas_rta_larga_a = rta_larga.resultados[-1]
        print(f"Valvulas Respuesta larga: {valvulas_rta_larga_a}")
        print(f"Medición respuesta larga: {medicion_rta_larga_a}")

    if True: # Pispear resultados por generador
        print("-"*10+"Generatriz"+"-"*10)
        rta_larga.generatriz()
        rta_larga.resultados.sort()
        print(f"Respuesta final larga (entre {len(rta_larga.resultados)}): ")    
        for i in rta_larga.resultados[:5] +["///"] +rta_larga.resultados[-5:]: print(i)
        print("/"*10+"Generatriz"+"/"*10)

        medicion_rta_larga_a, valvulas_rta_larga_a = rta_larga.resultados[-1]
        print(f"Valvulas Respuesta larga: {valvulas_rta_larga_a}")
        print(f"Medición respuesta larga: {medicion_rta_larga_a}")

    RespuestaA, RespuestaB = medicion_rta_larga_a, 'N/A'

    print("	La respuesta A es " + str(RespuestaA))
    print("That's not the right answer; your answer is too low. (You guessed 1318.)")
    print("	La respuesta B es " + str(RespuestaB))

