#!/usr/bin/env python3.10

numero="06"

archivoSolucion = numero+"-Solution.py"
inputlargoFile = "input"+numero+".txt"


with open(archivoSolucion, 'a') as file_object:
    file_object.write("#!/usr/bin/env python3.10\n\n\n")
    file_object.write("lines, largo=[], []\n")
    file_object.write("with open(\""+inputlargoFile+"\") as file_object:\n  lines = file_object.readlines()\n\n")
    file_object.write("for line in lines: \n  largo.append(line.rstrip())\n\n\n")
    file_object.write("""corto=[].split('\\n')\\n\\n""")
    file_object.write("RespuestaA, RespuestaB = 'N/A', 'N/A'\n\n\n")
    file_object.write('print("\tLa respuesta A es " + str(RespuestaA))\n')
    file_object.write('print("\tLa respuesta B es " + str(RespuestaB))\n')
