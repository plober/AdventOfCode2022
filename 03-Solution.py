#!/usr/bin/env python3.10


lines, largo=[], []
with open("input03.txt") as file_object:
  lines = file_object.readlines()

for line in lines:
  largo.append(line.rstrip())


corto=[]



RespuestaCortaA, RespuestaA, RespuestaCortaB, RespuestaB = 'N/A', 'N/A', 'N/A', 'N/A'


print("	La respuesta del Ejemplo A es " + str(RespuestaCortaA))
print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta del Ejemplo B es " + str(RespuestaCortaB))
print("	La respuesta B es " + str(RespuestaB))
