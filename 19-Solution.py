#!/usr/bin/env python3.10


largo = [line.rstrip() for line in open("input19.txt")]

corto = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".splitlines()


class NotEnoughMinerals:
    def __init__(self, input):
        blueprint = {}

        for renglon in input:
            # renglon = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."
            _, numero, _, _, _, _, ore_robot_ore_cost, _, _, _, _, _, clay_robot_ore_cost, _, _, _, _, _, obsidian_robot_ore_cost, _, _, obsidian_robot_clay_cost, _, _, _, _, _, geode_robot_ore_cost, _, _, geode_robot_obsidian_cost, _ = renglon.split()
            blueprint[int(numero[:-1])] = (int(ore_robot_ore_cost),
                                           int(clay_robot_ore_cost),
                                           int(obsidian_robot_ore_cost),
                                           int(obsidian_robot_clay_cost),
                                           int(geode_robot_ore_cost),
                                           int(geode_robot_obsidian_cost))
        self.blueprints = blueprint

    def calcular_rendimiento(self, costos: tuple[int, int, int, int, int, int], tiempo_minutos=24, verbose=True) -> int:
        # Setear costos
        ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost = costos
        # Setear robots disponibles
        robot_ore, robot_clay, robot_obsidiana, robot_geode = 1, 0, 0, 0
        # Setear robots en construcción
        ore_robot_en_contruccion, clay_robot_en_contruccion, obsidian_robot_en_contruccion, geode_robot_en_contruccion = 0, 0, 0, 0
        # Setear Ores disponibles
        recurso_clay, recurso_ore, recurso_obsidiana, recurso_geode = 0, 0, 0, 0

        for minutos in range(tiempo_minutos):

            if verbose:
                print(f"\n== Minute {minutos+1} ==")
            # Construcción

            if geode_robot_ore_cost <= recurso_ore and geode_robot_obsidian_cost <= recurso_obsidiana:
                geode_robot_en_contruccion = 1
                recurso_ore -= geode_robot_ore_cost
                recurso_obsidiana -= geode_robot_obsidian_cost
                if verbose:
                    print(
                        f"Spend {geode_robot_ore_cost} ore and {geode_robot_obsidian_cost} obsidian to start building a geode-cracking robot.")

            if obsidian_robot_ore_cost <= recurso_ore and obsidian_robot_clay_cost <= recurso_clay:
                obsidian_robot_en_contruccion = 1
                recurso_ore -= obsidian_robot_ore_cost
                recurso_clay -= obsidian_robot_clay_cost
                if verbose:
                    print(
                        f"Spend {obsidian_robot_ore_cost} ore and {obsidian_robot_clay_cost} clay to start building an obsidian-collecting robot.")

            if clay_robot_ore_cost <= recurso_ore:
                clay_robot_en_contruccion = 1
                recurso_ore -= clay_robot_ore_cost
                if verbose:
                    print(
                        f"Spend {clay_robot_ore_cost} clay to start building a clay-collecting robot.")

            if ore_robot_ore_cost <= recurso_ore:
                ore_robot_en_contruccion = 1
                recurso_ore -= ore_robot_ore_cost
                if verbose:
                    print(
                        f"Spend {ore_robot_ore_cost} ore to start building a ore-collecting robot.")

            # Recolección
            recurso_ore += robot_ore
            recurso_clay += robot_clay
            recurso_obsidiana += robot_obsidiana
            recurso_geode += robot_geode
            if verbose:
                print(
                    f"{robot_ore} ore-collecting robots collects {robot_ore} ore; you now have {recurso_ore} ore.")
                if robot_clay > 0:
                    print(
                        f"{robot_clay} clay-collecting robots collects {robot_clay} clay; you now have {recurso_clay} clay.")
                if robot_obsidiana > 0:
                    print(
                        f"{robot_obsidiana} obsidiana-collecting robots collects {robot_obsidiana} obsidiana; you now have {recurso_obsidiana} obsidiana.")
                if robot_geode > 0:
                    print(
                        f"{robot_geode} geode-cracking robots crack {robot_geode} geode; you now have {recurso_geode} geode.")

            # Construcción finalizada
            if ore_robot_en_contruccion == 1:
                ore_robot_en_contruccion = 0
                robot_ore += 1
                if verbose:
                    print(
                        f"The new ore-collecting robot is ready; you now have {robot_ore} of them.")

            if clay_robot_en_contruccion == 1:
                clay_robot_en_contruccion = 0
                robot_clay += 1
                if verbose:
                    print(
                        f"The new clay-collecting robot is ready; you now have {robot_clay} of them.")

            if obsidian_robot_en_contruccion == 1:
                obsidian_robot_en_contruccion = 0
                robot_obsidiana += 1
                if verbose:
                    print(
                        f"The new obsidian-collecting robot is ready; you now have {robot_obsidiana} of them.")

            if geode_robot_en_contruccion == 1:
                geode_robot_en_contruccion = 0
                robot_geode += 1
                if verbose:
                    print(
                        f"The new geode-cracking robot is ready; you now have {robot_geode} of them.")

        return recurso_geode

    def generar_cadenas(self,
                        costos: tuple[int, int, int, int, int, int],
                        recursos: list[int] = [0, 0, 0, 0],
                        robots_disponibles: list[int] = [1, 0, 0, 0],
                        construction_history: list[str] = [],
                        tiempo_minutos=0,
                        verbose=True):
        """Toma un estado, evalúa las posibilidades y branchea de ser posible."""

        # Setear costos
        ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost = costos
        # Setear Ores disponibles
        recurso_ore, recurso_clay, recurso_obsidiana, recurso_geode = recursos
        # Setear robots disponibles
        robot_ore, robot_clay, robot_obsidiana, robot_geode = robots_disponibles

        # Verificar posible construcción de robots
        posible_robot_ore = 1 if ore_robot_ore_cost >= recurso_ore else 0
        posible_robot_clay = 1 if clay_robot_ore_cost >= recurso_ore else 0
        posible_robot_obsidian = 1 if obsidian_robot_ore_cost >= recurso_ore and obsidian_robot_clay_cost >= recurso_clay else 0
        posible_robot_geode = 1 if geode_robot_ore_cost >= recurso_ore and geode_robot_obsidian_cost >= recurso_obsidiana else 0

        posibles_robots = [posible_robot_ore, posible_robot_clay,
                           posible_robot_obsidian, posible_robot_geode]

        # Recolección
        recurso_ore += robot_ore
        recurso_clay += robot_clay
        recurso_obsidiana += robot_obsidiana
        recurso_geode += robot_geode

        def construir_bot(tipo_de_robot: str, recursos: list[int]) -> tuple[list[int], list[int], list[str]]:
            """Recibe el robot a construir y devuelve (recursos, robots y construction history)"""
            recursos_restantes = recursos.copy()
            robots_restantes = posibles_robots.copy()
            ore, clay, obs, geode = 0, 1, 2, 3
            if tipo_de_robot == "robot_ore":
                robots_restantes[0] += 1
                recursos_restantes[ore] = recursos[ore] - ore_robot_ore_cost
            elif tipo_de_robot == "robot_clay":
                robots_restantes[1] += 1
                recursos_restantes[ore] = recursos[ore] - clay_robot_ore_cost
            elif tipo_de_robot == "robot_obsidiana":
                robots_restantes[2] += 1
                recursos_restantes[ore] = recursos[ore] - obsidian_robot_ore_cost
                recursos_restantes[clay] = recursos[clay] - obsidian_robot_clay_cost
            else:  # tipo == "robot_geode"
                robots_restantes[3] += 1
                recursos_restantes[ore] = recursos[ore] - geode_robot_ore_cost
                recursos_restantes[obs] = recursos[obs] - geode_robot_obsidian_cost

            return recursos_restantes, robots_restantes, construction_history + [tipo_de_robot]
        
        # branchear
        if posible_robot_geode:
            tipo = "posible_robot_geode"
            nuevos_recursos, nuevos_robots, longer_construction_history = construir_bot(tipo, recursos)
            self.generar_cadenas(costos, nuevos_recursos, nuevos_robots,
                                    longer_construction_history, tiempo_minutos + 1, verbose)
        if posible_robot_obsidian:
            tipo = "posible_robot_obsidian"
            nuevos_recursos, nuevos_robots, longer_construction_history = construir_bot(tipo, recursos)
            self.generar_cadenas(costos, nuevos_recursos, nuevos_robots,
                                    longer_construction_history, tiempo_minutos + 1, verbose)
        if posible_robot_clay:
            tipo = "robot_clay"
            nuevos_recursos, nuevos_robots, longer_construction_history = construir_bot(tipo, recursos)
            self.generar_cadenas(costos, nuevos_recursos, nuevos_robots,
                                    longer_construction_history, tiempo_minutos + 1, verbose)
        if posible_robot_ore:
            tipo = "robot_ore"
            nuevos_recursos, nuevos_robots, longer_construction_history = construir_bot(tipo, recursos)
            self.generar_cadenas(costos, nuevos_recursos, nuevos_robots,
                                 longer_construction_history, tiempo_minutos + 1, verbose)
        # Alternativa opción de "no construir nada"
        self.generar_cadenas(costos, recursos, robots_disponibles, construction_history, tiempo_minutos + 1, verbose)

        

        if verbose:
            print(
                f"{robot_ore} ore-collecting robots collects {robot_ore} ore; you now have {recurso_ore} ore.")
            if robot_clay > 0:
                print(
                    f"{robot_clay} clay-collecting robots collects {robot_clay} clay; you now have {recurso_clay} clay.")
            if robot_obsidiana > 0:
                print(f"{robot_obsidiana} obsidiana-collecting robots collects {robot_obsidiana} obsidiana; you now have {recurso_obsidiana} obsidiana.")
            if robot_geode > 0:
                print(
                    f"{robot_geode} geode-cracking robots crack {robot_geode} geode; you now have {recurso_geode} geode.")
        condicion_de_cierre = (tiempo_minutos >= 24)
        if condicion_de_cierre: return construction_history

    def respuesta_a(self) -> int:
        respuesta_final = 0
        for key in self.blueprints:
            print()
            print("/"*5+f" Calculo para {key} "+"/"*5)
            resultado = self.calcular_rendimiento(self.blueprints[key])
            print(f"\tCalidad para {key}: {resultado}")
            respuesta_final += key * resultado
        print()
        return respuesta_final


Respuesta_Corta = NotEnoughMinerals(corto)
# Respuesta_Corta.respuesta_a()

Respuesta_Larga = NotEnoughMinerals(largo)
for plano in Respuesta_Larga.blueprints:
    costo = Respuesta_Larga.blueprints[plano]
    print(f"Blueprint {plano}: {costo}")
    print(f"\t ASAP Geode = {costo[5]}:")

RespuestaA, RespuestaB = 'N/A', 'N/A'

print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
