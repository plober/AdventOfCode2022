#!/usr/bin/env python3.10


largo = [line.rstrip() for line in open("input10.txt")]
casi_corto = [cortalina.rstrip() for cortalina in open("input10corto.txt")]

corto = """noop
addx 3
addx -5""".splitlines()


class CathodeRayTube:
    """Intento simple de medior X en funcion de los ciclos"""

    def __init__(self, instrucciones):
        self.registro = [1]
        self.instrucciones = instrucciones
        # self.registro.extend([] for i in range(instrucciones))
        self.pantalla = ["."] * (40*6+1)
        self.parsear_instrucciones(instrucciones)
        # for i in range(len(instrucciones)):
        #     print("{}: {}, {}".format(i, self.registro[i], instrucciones[i]))

    def parsear_instrucciones(self, instrucciones):
        for comando in instrucciones:
            # comando = "addx -14"
            self.registro.extend(
                [0, int(comando[5:])] if comando.startswith("a") else [0])
            # print("parseando ciclo {}: {}, {}".format(
            #     numero, sum(self.registro), comando))
        print("Ya basta")

    def medir_registro_X(self, cantidad):
        return (sum(self.registro[:cantidad]))

    def fuerza_señal_X(self, cantidad):
        # relevantes = [q for q in range(20,221,40)]
        return self.medir_registro_X(cantidad) * cantidad

    def barrido_crt(self):
        rolling_sum = 0
        print(self.registro)
        for centro in range(len(self.registro)):
            rolling_sum += self.registro[centro]
            iluminado = (centro - 1) <= rolling_sum <= (centro + 1)
            print("{},{}".format(len(self.pantalla), centro))
            self.pantalla[centro] = "#" if iluminado else "_"
        self.mostrar_pantalla() 

    def mostrar_pantalla(self):
        [print("".join(self.pantalla[i:i+40])) for i in range(0, 241, 40)]
        # print("".join(self.pantalla))


respuesta_muy_corta = CathodeRayTube(corto)
assert respuesta_muy_corta.medir_registro_X(1) == 1
assert respuesta_muy_corta.medir_registro_X(2) == 1
assert respuesta_muy_corta.medir_registro_X(3) == 1
assert respuesta_muy_corta.medir_registro_X(4) == 4
assert respuesta_muy_corta.medir_registro_X(5) == 4

# print([respuesta_casi_corta.fuerza_señal_X( q) for q in range(20,221,40)])

respuesta_casi_corta = CathodeRayTube(casi_corto)

# print("Comienzo Casi_corta: {}".format(respuesta_casi_corta.instrucciones))
# print("Prueba respuesta {}, {}".format(
#     20, respuesta_casi_corta.medir_registro_X(20)))
# print("Prueba respuesta {}, {}".format(
#     60, respuesta_casi_corta.medir_registro_X(60)))
# print("Prueba respuesta {}, {}".format(
#     100, respuesta_casi_corta.medir_registro_X(100)))
# print("Prueba respuesta {}, {}".format(
#     140, respuesta_casi_corta.medir_registro_X(140)))
# print("Prueba respuesta {}, {}".format(
#     180, respuesta_casi_corta.medir_registro_X(180)))
# print("Prueba respuesta {}, {}".format(
#     220, respuesta_casi_corta.medir_registro_X(220)))

assert respuesta_casi_corta.medir_registro_X(20) == 21
assert respuesta_casi_corta.medir_registro_X(60) == 19
assert respuesta_casi_corta.medir_registro_X(100) == 18
assert respuesta_casi_corta.medir_registro_X(140) == 21
assert respuesta_casi_corta.medir_registro_X(180) == 16
assert respuesta_casi_corta.medir_registro_X(220) == 18

assert respuesta_casi_corta.fuerza_señal_X(20) == 420
assert respuesta_casi_corta.fuerza_señal_X(60) == 1140
assert respuesta_casi_corta.fuerza_señal_X(100) == 1800
assert respuesta_casi_corta.fuerza_señal_X(140) == 2940
assert respuesta_casi_corta.fuerza_señal_X(180) == 2880
assert respuesta_casi_corta.fuerza_señal_X(220) == 3960

rta_casi_corta = 0
for q in range(20, 221, 40):
    rta_casi_corta += respuesta_casi_corta.fuerza_señal_X(q)

assert rta_casi_corta == 13140
respuesta_casi_corta.mostrar_pantalla()


print("\tRespuesta casi corta {}".format(rta_casi_corta))

respuesta_larga = CathodeRayTube(largo)
RespuestaA = 0
for q in range(20, 221, 40):
    RespuestaA += respuesta_larga.fuerza_señal_X(q)


RespuestaB = 'N/A'

print("	La respuesta A es " + str(RespuestaA))
print("         (You guessed 13140) That's not the right answer; your answer is too high")
print("	La respuesta B es " + str(RespuestaB))
