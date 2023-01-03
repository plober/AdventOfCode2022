#!/usr/bin/env python3.10


lines, largo=[], []
with open("input07.txt") as file_object:
  lines = file_object.readlines()

for line in lines: 
  largo.append(line.rstrip())


corto="""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".split('\n')

class CumulativeSize:
    """Intento simple de obtener los tamaños de directorios"""

    def __init__(self, lista_de_comandos):
        """Inicializa clase, lee directorios"""
        self.lista_de_comandos = lista_de_comandos
        self.diccionario_paths={"/":0}
        path="/"
        directorio="/"
        caminito=[path]
        vidente = False
        for comando in self.lista_de_comandos[1:]:
            print("Corriendo "+comando) if vidente else ""
            if comando == "$ cd ..":
                path = path.removesuffix(directorio+"/")
                directorio = path.split("/")[-2]
                caminito = caminito[:-1]
            elif comando.startswith("$ cd "):
                directorio = comando[5:]
                path += directorio + "/"
                self.diccionario_paths[path]=0
                caminito.append(path)
            elif comando.startswith("$ ls"):
                pass
            elif comando.startswith("dir "):
                pass
            else:
                tamaño_archivo = int(comando.split()[0])
                for rastro in caminito:
                    self.diccionario_paths[rastro] += tamaño_archivo
            if vidente:
                print("    path: " + path)
                print("    dir : " + directorio)
                print("    ",end="")
                print(self.diccionario_paths)

    def mostrar_arbol(self):
        total=[]
        self.diccionario_paths["<----------"]=8_381_164
        for key in self.diccionario_paths:
            #'{: >9s}, World'.format('Hello')
            # print('{: >9}'.format(self.diccionario_paths[key]), key)
            total.append([self.diccionario_paths[key], key])
        total.sort()
        for numero in total:
            print (numero)

    def suma_menores_a_100k(self):
        total = sum([tamaño if tamaño <= 100_000 else 0 for _ , tamaño in self.diccionario_paths.items()])
        # sum([numero if numero > 50 else 0 for numero in range(100)])
        # for key, value in d.items():
        #     print(key, value)
        return total

    def justo_encima_de(self):
        objetivo = 30000000 - (70_000_000 - self.diccionario_paths["/"])
        #print("X value is: {x_val}. Y value is: {y_val}.".format(x_val=2, y_val=3))
        print("{total} de espacio total, {ocupado} espacio ocupado, {libre} espacio libre, {necesario} de espacio necesario, {objetivo} espacio que es necesario borrar".format( \
            total= "70.000.000", \
            ocupado = self.diccionario_paths["/"], \
            libre = 70_000_000 - self.diccionario_paths["/"], \
            necesario = "30.000.000" , \
            objetivo = 30000000 - (70_000_000 - self.diccionario_paths["/"])))
        return min([tamaño for _ , tamaño in self.diccionario_paths.items() if tamaño >= objetivo])


respuestas_cortas = CumulativeSize(corto)
respuestas_cortas.mostrar_arbol()
print("---")

assert respuestas_cortas.diccionario_paths["/a/e/"] == 584
assert respuestas_cortas.diccionario_paths["/a/"] == 94853 
assert respuestas_cortas.diccionario_paths["/d/"] == 24933642
assert respuestas_cortas.diccionario_paths["/"] == 48381165
assert respuestas_cortas.suma_menores_a_100k() == 95437
respuestas_largas = CumulativeSize(largo) 
respuestas_largas.mostrar_arbol()
assert respuestas_cortas.justo_encima_de()==24_933_642, "Creía que era " +str(respuestas_cortas.justo_encima_de())


RespuestaA, RespuestaB = respuestas_largas.suma_menores_a_100k(), respuestas_largas.justo_encima_de()


print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
print(" La respuesta B no es 43_441_553, es menor")
print(" La respuesta B no es 10_646_799, es menor")
