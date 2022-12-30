#!/usr/bin/env python3.10


lines, largo=[], []
with open("input02.txt") as file_object:
  lines = file_object.readlines()

for line in lines: 
  largo.append(line.rstrip())


corto="""A Y
B X
C Z""".split("\n")

# A for Rock, B for Paper, and C for Scissors (them)
#
# The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) 
# plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won)"""


class PiedraPapelTijera:
    def suma_valores(instrucciones):
        # X for Rock, Y for Paper, and Z for Scissors (yo)
        diccionario_resultados = {
            'A X': 1 + 3, # Piedras, empate 
            'A Y': 2 + 6, # él Piedra, yo Papel: gané
            'A Z': 3 + 0, # él Piedra, yo Tijera: perdí
            'B X': 1 + 0, # él Papel, yo Piedra: Perdí
            'B Y': 2 + 3, # Papel, empate
            'B Z': 3 + 6, # él Papel, yo Tijera: gané
            'C X': 1 + 6, # él tijera, yo Piedra: gané
            'C Y': 2 + 0, # él tijera, , yo Papel: perdí
            'C Z': 3 + 3, # Tijeras, empate
            }
        resultados = []
        for round in instrucciones:
            resultados.append(diccionario_resultados[round])
        return sum(resultados)

    def suma_por_resultado(instrucciones):     
        # A for Rock, B for Paper, and C for Scissors (them)
        # (1 for Rock, 2 for Paper, and 3 for Scissors) 
        # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
        diccionario_intenciones = {
            'A X': 3 + 0, 
            'A Y': 1 + 3, 
            'A Z': 2 + 6, 
            'B X': 1 + 0, 
            'B Y': 2 + 3, 
            'B Z': 3 + 6, 
            'C X': 2 + 0, 
            'C Y': 3 + 3, 
            'C Z': 1 + 6, 
            }
        resultados = []
        for round in instrucciones:
            resultados.append(diccionario_intenciones[round])
        return sum(resultados)

assert PiedraPapelTijera.suma_valores(corto.copy())== 15
assert PiedraPapelTijera.suma_por_resultado(corto.copy())== 12
RespuestaA, RespuestaB = PiedraPapelTijera.suma_valores(largo), PiedraPapelTijera.suma_por_resultado(largo)
print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
