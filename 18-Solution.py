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

    def superficie_expuesta(self):
        conteo_caras = 0
        alrededor = [(1, 0, 0),
                     (-1, 0, 0),
                     (0, 1, 0),
                     (0, -1, 0),
                     (0, 0, 1),
                     (0, 0, -1),
                     ]
        caras_alrededor = set()
        caras_alrededor: set[tuple[int, int, int]]
        for gota in self.gotas_de_lava:
            conteo_caras += 6
            for cara in alrededor:
                if (gota[0] + cara[0],
                    gota[1] + cara[1],
                    gota[2] + cara[2]) in self.gotas_de_lava:
                    conteo_caras -=1
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

    def mostrar_como_cubos(self):
        import matplotlib.pyplot as plt
        import numpy as np

        plt.style.use('_mpl-gallery')

        # Prepare some coordinates
        x, y, z = np.indices((8, 8, 8))

        # Draw cuboids in the top left and bottom right corners
        cube1 = (x < 3) & (y < 3) & (z < 3)
        cube2 = (x >= 5) & (y >= 5) & (z >= 5)

        # Combine the objects into a single boolean array
        voxelarray = cube1 | cube2

        # Plot
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.voxels(voxelarray, edgecolor='k')

        ax.set(xticklabels=[],
               yticklabels=[],
               zticklabels=[])

        plt.show()


version_corta = BoilingBoulders(corto)
assert BoilingBoulders(corto).superficie_expuesta() == 64
# print(
#     f"Gotas de Lava ({len(version_corta.gotas_de_lava)})= {version_corta.gotas_de_lava}")
# print(
#     f"Superficie Expuesta = {version_corta.superficie_expuesta()}")

# print(f"corto_uno {len(BoilingBoulders(corto_uno).superficie_expuesta())}")
# print(f"corto_dos {len(BoilingBoulders(corto_dos).superficie_expuesta())}")
# print(f"corto_tres {len(BoilingBoulders(corto_tres).superficie_expuesta())}")

# print(f"Gotas de Lava corto_tres({          len(BoilingBoulders(corto_tres).gotas_de_lava)})= {BoilingBoulders(corto_tres).gotas_de_lava}")
# print(f"Superficie Expuesta corto_tres({    len(BoilingBoulders(corto_tres).superficie_expuesta())}) = {BoilingBoulders(corto_tres).superficie_expuesta()}")


# version_corta.mostrar_como_puntos(BoilingBoulders(corto_tres).gotas_de_lava)
# version_corta.mostrar_como_puntos(BoilingBoulders(corto_tres).superficie_expuesta())


RespuestaA, RespuestaB = (BoilingBoulders(largo).superficie_expuesta()), 'N/A'

print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
