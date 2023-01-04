#!/usr/bin/env python3.10

lines, largo=[], []
with open("input08.txt") as file_object:
  lines = file_object.readlines()

for line in lines: 
  largo.append(line.rstrip())


corto="""30373
25512
65332
33549
35390""".split('\n')

class TreeTopTarp:

    def __init__(self, plano):
        self.plano = plano
        self.largo = len(plano)
        self.traspuesto = self.trasponer(plano)
        self.bosque_visible=["_"* self.largo] * self.largo

    def trasponer(self, plano):
        traspuesto = ["" for _ in range(len(plano))]
        for fila in range(len(plano[0])):
            for columna in range(len(plano[fila])):
                traspuesto[fila] += plano[columna][fila]
        return traspuesto

    def visibilidad(self, ingreso, explica=False):
        conteo = 0
        plano_muestral =[]
        for renglon in ingreso:
            altura = -1 #reinicio por renglón
            muestra = ""
            for arbol in renglon:
                if int(arbol) > altura:
                    conteo += 1
                    altura = int(arbol)
                    muestra += arbol 
                else: 
                    muestra += "_"
            if explica: print(muestra)
            plano_muestral.append(muestra)
        return plano_muestral

    def visibles_desde_derecha(self, explica=False):
        arboles_visibles=0
        for renglon in self.visibilidad(self.plano, explica):
            arboles_visibles += len([arbol for arbol in renglon if arbol != "_"]) 
        return arboles_visibles

    def visibles_desde_izquierda(self, explica=False):
        arboles_visibles=0
        for renglon in self.visibilidad([linea[::-1] for linea in self.plano], explica):
            arboles_visibles += len([arbol for arbol in renglon if arbol != "_"]) 
        return arboles_visibles

    def visibles_desde_arriba(self, explica=False):
        arboles_visibles=0
        for renglon in self.visibilidad(self.traspuesto, explica):
            arboles_visibles += len([arbol for arbol in renglon if arbol != "_"]) 
        return arboles_visibles

    def visibles_desde_abajo(self, explica=False):
        arboles_visibles=0
        for renglon in self.visibilidad([linea[::-1] for linea in self.traspuesto], explica):
            arboles_visibles += len([arbol for arbol in renglon if arbol != "_"]) 
        return arboles_visibles

    def vision_360(self):
        """Mostrar plano y traspuesto"""
        desde_este, desde_oeste, desde_norte, desde_sur = [],[],[],[]

        for regla in self.visibilidad(self.plano):
            desde_oeste.append(regla)
        #     print(regla)
        # print("---")    
        for regla in self.visibilidad([linea[::-1] for linea in self.plano]):
            desde_este.append(regla)
        #     print(regla)
        # print("---")    
        for regla in self.visibilidad(self.traspuesto):
            desde_norte.append(regla)
        #     print(regla)
        # print("---")    
        for regla in self.visibilidad([linea[::-1] for linea in self.traspuesto]):
            desde_sur.append(regla)
            # print(regla)

        self.reemplazar_si_es_visible(desde_este, desde_oeste, desde_norte, desde_sur)
        return self.bosque_visible

    def reemplazar_si_es_visible(self, desde_este, desde_oeste, desde_norte, desde_sur):
        for i in range(self.largo):
            for j in range(self.largo):
                # Mandar a self.bosque_visible[i][j] lo que sea diferente de "_"
                desde_o, desde_e, desde_n, desde_s = desde_oeste[i][j] , desde_este[i][-j-1], desde_norte[j][i], desde_sur[j][-i-1]
                punto={desde_o, desde_e, desde_n, desde_s}
                if punto == {"_"}:
                    self.bosque_visible[i] = self.bosque_visible[i][:j] + "_" + self.bosque_visible[i][j+1:]
                elif len(punto - {"_"}) == 1:
                    nuevo = (punto - {"_"}).pop()
                    # try:
                    self.bosque_visible[i] = self.bosque_visible[i][:j] + nuevo + self.bosque_visible[i][j+1:]
                    # except IndexError as e:
                    #     print("Sucedió un IndexError, con el mensaje:", e)
                    #     print("Fila: {fila}, columna: {columna}, largo: {largo}".format(fila = i, columna = j, largo = self.largo))
                    #     for linea in self.bosque_visible:
                    #         print(linea)
                    #     print("Fin")
                else:
                    # print("X value is: {x_val}. Y value is: {y_val}.".format(x_val=2, y_val=3))
                    print("Fila: {fila}, columna: {columna}, valor preciso: {posta}".format(fila = i, columna = j, posta = self.plano[i][j]))
                    print(punto)
                    print("Desde oeste: "+ desde_o)
                    print("Desde este: "+ desde_e) 
                    print("Desde norte: "+ desde_n) 
                    print("Desde sur: "+ desde_s)
                    print("-"*5)

    def mostrar_bosque(self):
        for renglon in self.vision_360():
            print(renglon)

    def contar_visibles(self):
        conteo = 0
        for renglon in self.bosque_visible:
            for arbol_visible in renglon:
                if arbol_visible != "_": conteo += 1
        return conteo

respuestas_cortas = TreeTopTarp(corto)
respuestas_cortas.vision_360()
respuestas_cortas.mostrar_bosque()
print ("-"*5)
assert respuestas_cortas.visibles_desde_derecha()==11,  "Desde la Derecha se tendrían que ver 11 y se ven "+str(respuestas_cortas.visibles_desde_derecha(True))
assert respuestas_cortas.visibles_desde_izquierda()==11,"Desde la Izquierda se tendrían que ver 11 y se ven "+str(respuestas_cortas.visibles_desde_izquierda(True))
assert respuestas_cortas.visibles_desde_arriba()==10,   "Desde Arriba se tendrían que ver 10 y se ven "+str(respuestas_cortas.visibles_desde_arriba(True))
assert respuestas_cortas.visibles_desde_abajo()==8,     "Desde Abajo se tendrían que ver 8 y se ven "+str(respuestas_cortas.visibles_desde_abajo(True))
assert respuestas_cortas.contar_visibles() == 21, "Deberían verse 21 y se ven"

respuestas_largas = TreeTopTarp(largo)
respuestas_largas.vision_360()
respuestas_largas.mostrar_bosque()

RespuestaA, RespuestaB = respuestas_largas.contar_visibles(), 'N/A'

print("	La respuesta A es " + str(RespuestaA))
print("	La respuesta B es " + str(RespuestaB))
