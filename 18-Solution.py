#!/usr/bin/env python3.10


largo = [line.rstrip() for line in open("input18.txt")]
corto = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".splitlines()
corto_uno = ["1,1,1"]
corto_dos = """2,2,2
1,2,2""".splitlines()
corto_tres = """2,2,2
1,2,2
1,1,2""".splitlines()


class BoilingBoulders:

    def __init__(self, input: list[str]):
        gotas_de_lava = set()
        gotas_de_lava: set[tuple[int, int, int]]

        for gota in input:
            x, y, z = gota.split(",")
            gotas_de_lava.add((int(x), int(y), int(z)))
        self.gotas_de_lava = gotas_de_lava
        self.alrededor = [(1, 0, 0),
                          (-1, 0, 0),
                          (0, 1, 0),
                          (0, -1, 0),
                          (0, 0, 1),
                          (0, 0, -1),
                          ]

    def superficie_expuesta(self, volumen: set[tuple[int, int, int]]) -> int:
        conteo_caras = 0

        for gota in volumen:
            conteo_caras += 6
            for cara in self.alrededor:
                if (gota[0] + cara[0],
                    gota[1] + cara[1],
                        gota[2] + cara[2]) in volumen:
                    conteo_caras -= 1
        return conteo_caras

    def mostrar_como_puntos(self, input=[]):
        import matplotlib.pyplot
        if input == []:
            input = self.gotas_de_lava

        matplotlib.pyplot.style.use('_mpl-gallery')

        # Make data

        xs = [x_gotas for x_gotas, y_gotas, z_gotas in input]
        ys = [y_gotas for x_gotas, y_gotas, z_gotas in input]
        zs = [z_gotas for x_gotas, y_gotas, z_gotas in input]

        # Plot
        fig, ax = matplotlib.pyplot.subplots(subplot_kw={"projection": "3d"})
        ax.scatter(xs, ys, zs)

        ax.set(xticklabels=[],
               yticklabels=[],
               zticklabels=[])

        return matplotlib.pyplot.show()

    def espacio_negativo(self, investigar : set[tuple[int, int, int]]) -> set[tuple[int, int, int]]:
        """Recibe un set de coordenadas y devuelve la figura que esté dentro sin tomar en cuenta huecos."""
        maximo = max([max(x,y,z) for x,y,z in investigar])
        iterador = [i for i in range(maximo + 1)]
        espacio_total = set()
        espacio_total: set[tuple[int, int, int]]

        for xs in iterador:
            for ys in iterador:
                for zs in iterador:
                    espacio_total.add((xs, ys, zs))

        encavernado = espacio_total - self.gotas_de_lava

        puntos_conectados = {(1, 1, 1)}
        recien_incorporados = {(1, 1, 1)}
        cuenta = 0

        while len(recien_incorporados) != 0 and cuenta < 400:
            cuenta += 1
            # print(f"Tengo {len(recien_incorporados)} recién incorporados")
            capaz_interesantes = set()

            for lugar in recien_incorporados:
                for explorar in self.alrededor:
                    capaz_interesantes.add(
                        (explorar[0] + lugar[0], explorar[1] + lugar[1], explorar[2] + lugar[2]))
                    # Carga todos los puntos alrededor de recien_incorporados a capaz_interesantes
            a_incorporar = capaz_interesantes & encavernado - puntos_conectados
            # Los puntos a incorporar son los que estaban alrededor de los recién incorporados, pero
            #     solo si están dentro del cubo a evaluar, y quitándole los que ya sé que están dentro
            # print(f"Tengo {len(a_incorporar)} a incorporar")

            # agrega los recién encontrados a los puntos ya conocidos
            puntos_conectados |= a_incorporar
            recien_incorporados = a_incorporar

        return espacio_total - puntos_conectados
    
    def respuesta_b (self):
        return self.superficie_expuesta(self.espacio_negativo(self.gotas_de_lava))
        pass

RespuestaCorta = BoilingBoulders(corto)
assert RespuestaCorta.superficie_expuesta(RespuestaCorta.gotas_de_lava) == 64
assert RespuestaCorta.respuesta_b() == 58



print("/"*10)
RespuestaLarga = BoilingBoulders(largo)

mostrar_grafico = False
if mostrar_grafico:
    RespuestaCorta.mostrar_como_puntos(RespuestaCorta.espacio_negativo(RespuestaCorta.gotas_de_lava))
    RespuestaLarga.mostrar_como_puntos()

RespuestaA, RespuestaB = (RespuestaLarga.superficie_expuesta(RespuestaLarga.gotas_de_lava)), RespuestaLarga.respuesta_b()

print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
