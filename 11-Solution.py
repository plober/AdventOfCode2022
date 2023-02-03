#!/usr/bin/env python3.10


largo = [line.rstrip() for line in open("input11.txt")]

corto = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".splitlines()


class MonkeyInTheMiddle:
    def __init__(self, input: list):
        lista_de_monos = [(input[0+a*7:6+a*7]) for a in range(len(input)//7+1)]
        self.diccionario_de_monos = {}
        self.tranquilizacion = 3
        self.round = 1
        self.pases = {"de 0 a 0": 0,
                      "de 1 a 0": 0,
                      "de 2 a 0": 0,
                      "de 3 a 0": 0,
                      "de 0 a 1": 0,
                      "de 1 a 1": 0,
                      "de 2 a 1": 0,
                      "de 3 a 1": 0,
                      "de 0 a 2": 0,
                      "de 1 a 2": 0,
                      "de 2 a 2": 0,
                      "de 3 a 2": 0,
                      "de 0 a 3": 0,
                      "de 1 a 3": 0,
                      "de 2 a 3": 0,
                      "de 3 a 3": 0,
                      }

        self.divisor = 1
        for registro_mono in lista_de_monos:
            self.diccionario_de_monos[int(registro_mono[0][7:-1])] = {
                # Starting items: 69, 86, 67, 55, 96, 69, 94, 85
                "lista_items": [int(item) for item in registro_mono[1][17:].split(",")],
                # # Operation: new = old + 3
                "operation": registro_mono[2][19:],
                # divisor = Test: divisible by 17
                "divisor": int(registro_mono[3][21:]),
                # tira_si_True  = "If true: throw to monkey 0"
                # tira_si_False = "If false: throw to monkey 1"
                "tira_si_True": int(registro_mono[4][29:]),
                "tira_si_False": int(registro_mono[5][29:]),
                "inspecciones": 0
            }
            self.divisor = self.divisor * int(registro_mono[3][21:])

    def get_monkey_status(self, monkey_id=0):
        """Monkey 1:
                Starting items: 54, 65, 75, 74
                Operation: new = old + 6
                Test: divisible by 19
                    If true: throw to monkey 2
                    If false: throw to monkey 0"""
        datos = self.diccionario_de_monos[monkey_id]
        estado = []
        estado.append(f"Monkey {monkey_id}:")
        estado.append(
            f"  Held items: {                 datos['lista_items']    }")
        estado.append(
            f"  Operation: new = {            datos['operation']      }")
        estado.append(
            f"  Test: divisible by {          datos['divisor']        }")
        estado.append(
            f"   If true: throw to monkey {   datos['tira_si_True']   }")
        estado.append(
            f"   If false: throw to monkey {  datos['tira_si_False']  }")
        estado.append(
            f"   Inspecciones {               datos['inspecciones']  }")
        print([print(linea) for linea in estado])
        return datos

    def monkey_round(self):
        self.round += 1
        [self.monkey_turn(key) for key in self.diccionario_de_monos]

    def every_monkey_status(self):
        [self.get_monkey_status(key) for key in self.diccionario_de_monos]
        print(
            [f' Monkey {key}: inspecciones {self.diccionario_de_monos[key]["inspecciones"]}' for key in self.diccionario_de_monos])

    def monkey_turn(self, monkey_id, vidente=False):
        datos_monos = self.diccionario_de_monos[monkey_id]
        # {
        # 'lista_items': [79, 98],
        # 'operation': 'old * 19',
        # 'divisor': 23,
        # 'tira_si_True': 2,
        # 'tira_si_False': 3
        # }
        if vidente:
            print(f"Monkey {monkey_id}:")

        while len(datos_monos['lista_items']) > 0:
            # assert datos_monos['inspecciones'] < 60000, f"Demasiadas inspecciones"

            if vidente:
                print(f" Inspects item {datos_monos['lista_items'][0]}")
            datos_monos['inspecciones'] += 1

            item = (self.incremento_preocupacion(datos_monos['lista_items'].pop(
                0), datos_monos['operation']) // self.tranquilizacion) % self.divisor
            if (item % datos_monos['divisor']) == 0:
                self.diccionario_de_monos[datos_monos['tira_si_True']]['lista_items'].append(
                    item)
                # self.pases[f"de {monkey_id} a {datos_monos['tira_si_True']}"] += 1
            else:
                self.diccionario_de_monos[datos_monos['tira_si_False']]['lista_items'].append(
                    item)
                # self.pases[f"de {monkey_id} a {datos_monos['tira_si_False']}"] += 1

            # item = (self.incremento_preocupacion(datos_monos['lista_items'].pop(0),
            #                                      datos_monos['operation']) // self.tranquilizacion) % (2*3*5*7*11*13*17*19)
            # if vidente:
            #     print(f"  New Value: {item}")

            # self.diccionario_de_monos[datos_monos[['tira_si_False', 'tira_si_True'][(
            #     item % datos_monos['divisor'] == 0)]]]['lista_items'].append(item)
                # Por oneliners como este es que demoro en aprender python ^^
                # pero se puede, mierda!

    def incremento_preocupacion(self, old: int, instruccion: str):
        # 'operation': 'old * 19',
        # 'operation': 'old + 3'
        if instruccion.endswith("old"):
            # , pero mantiene sus factores así que no es necesario
            return (old * old)
        return (old + int(instruccion[6:])) if '+' in instruccion else (old * int(instruccion[6:]))

    def top_two_monkey_business_level(self):
        best, bestest = sorted([self.diccionario_de_monos[key]["inspecciones"]
                               for key in self.diccionario_de_monos])[-2:]
        return best * bestest

    def rta_A(self):
        [self.monkey_round() for _ in range(20)]
        return self.top_two_monkey_business_level()

    def rta_B(self, vidente=False):
        self.tranquilizacion = 1
        for round in range(10000):
            # if round in [1, 20, 1000]:
            if round in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
                print(f"\n== After round {round} ==")
                [print(f"Monkey {monkey_id} inspected items {self.diccionario_de_monos[monkey_id]['inspecciones']} times.")
                 for monkey_id in self.diccionario_de_monos]
                # for key, value in self.pases.items():
                #     if value > 0: print(f"{key}: {value}")

            self.monkey_round()

        return self.top_two_monkey_business_level()


monos_para_A = MonkeyInTheMiddle(corto)
respuesta_a_corta = monos_para_A.rta_A()
assert respuesta_a_corta == 10605, f"Respuesta a corta debe ser 10605 y no {respuesta_a_corta}"
print(f"Respuesta A corta obtenida")

monos_para_B = MonkeyInTheMiddle(corto)
respuesta_b_corta = monos_para_B.rta_B()
assert respuesta_b_corta == 2713310158, f"Respuesta B corta debe ser 2713310158 y no {respuesta_b_corta}"
print(f"Respuesta B corta obtenida")


señores_monos_A = MonkeyInTheMiddle(largo)
RespuestaA = señores_monos_A.rta_A()
assert RespuestaA == 56595, f"Respuesta a corta debe ser 56595 y no {RespuestaA}"

señores_monos_B = MonkeyInTheMiddle(largo)
RespuestaB = señores_monos_B.rta_B()

print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
