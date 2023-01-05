#!/usr/bin/env python3.10


lines, largo=[], []
with open("input06.txt") as file_object:
  largo = file_object.readlines()

largo = largo[0].rstrip()

class TunningTrouble:
    def repetidos(cadena,cantidad=4):
        # string = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
        # print(cadena)
        ocurrencia_en_caracter = 0
        for observando in range(cantidad, len(cadena)):
            if len(set([char for char in cadena[observando-cantidad:observando]])) == cantidad:
                # print("encontrado en "+ str(observando))
                ocurrencia_en_caracter = observando
                break            
        return ocurrencia_en_caracter


assert TunningTrouble.repetidos("mjqjpqmgbljsphdztnvjfqwrcgsmlb"        ) ==  7
assert TunningTrouble.repetidos("bvwbjplbgvbhsrlpgdmjqwftvncz"          ) ==  5
assert TunningTrouble.repetidos("nppdvjthqldpwncqszvftbrmjlhg"          ) ==  6
assert TunningTrouble.repetidos("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"     ) == 10
assert TunningTrouble.repetidos("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"      ) == 11

assert TunningTrouble.repetidos("mjqjpqmgbljsphdztnvjfqwrcgsmlb"    ,14 ) == 19
assert TunningTrouble.repetidos("bvwbjplbgvbhsrlpgdmjqwftvncz"      ,14 ) == 23
assert TunningTrouble.repetidos("nppdvjthqldpwncqszvftbrmjlhg"      ,14 ) == 23
assert TunningTrouble.repetidos("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg" ,14 ) == 29
assert TunningTrouble.repetidos("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"  ,14 ) == 26


RespuestaA, RespuestaB = TunningTrouble.repetidos(largo),  TunningTrouble.repetidos(largo,14)

print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
