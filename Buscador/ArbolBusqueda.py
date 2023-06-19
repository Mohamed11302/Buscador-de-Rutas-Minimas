#!/usr/bin/python3
import math
import CargarDatos
import CargarProblema
from queue import PriorityQueue

ListaNodos = CargarDatos.ListaNodos
DiccionarioAristas = CargarDatos.DiccionarioAristas

class NodoBusqueda:

    def __init__(self, id, padre, estado, valor, profundidad, costo, heuristica, accion):
        self.id = id
        self.nodoPadre = padre
        self.costo = costo
        self.profundidad = profundidad
        self.estado = estado
        self.accion = accion
        self.heuristica = heuristica
        self.valor = valor

    def __lt__(self, other):
        if self.getValor() == other.getValor():
            return self.getID() < other.getID()
        return self.getValor() < other.getValor()

    def getID(self):
        return self.id

    def getCosto(self):
        return self.costo

    def getProfundidad(self):
        return self.profundidad

    def getValor(self):
        return self.valor
    
    def getHeuristica(self):
        return self.heuristica

    def getEstado(self):
        return self.estado

    def getPadre(self):
        return self.nodoPadre    

    def camino(self,nodo,camino):
        camino.append(nodo)
        if nodo.getID() == 0:
            return camino
        else:
            return self.camino(nodo.getPadre(),camino)

    def print(self):
        cadena = ("["+str(self.getID())+"][{:.2f},[".format(self.getCosto())+str(self.getEstado().print())+"|" + self.getEstado().IDEstado[-6:]+"]")
        if self.getPadre() == None:
            cadena = cadena + ",None,"
        else:
            cadena = cadena +","+str(self.getPadre().getID())+","
        if self.accion == None:
            cadena = cadena + "None,"
        else:
            cadena = cadena + str(self.accion[0])+ "->" +str(self.accion[1]) + ","
        cadena = cadena + str(self.getProfundidad())+ ",{:.2f}".format(self.getHeuristica())+ ",{:.2f}".format(self.getValor(), 2)+"]" 
        return cadena

class Visitados:
    def __init__(self):
        self.visitados = set()

    def Insercion(self, estado): # Metodo para ingresar elementos
        if self.Pertenece(estado) == False:
            self.visitados.add(estado.IDEstado)
   
    def Pertenece(self,estado): # Metodo para buscar elementos
        return estado.IDEstado in self.visitados


def valorEstrategia(estrategia, id, profundidad, costo, heuristica):
    if estrategia == 'Breadth':
        if id == 0:
            valor = 0
        else:
            valor = profundidad
    elif estrategia == 'Depth':
        if id == 0:
            valor = 1
        else:
            valor = round(1/(profundidad+1), 2)
    elif estrategia == 'Uniform':
        if id == 0:
            valor = 0
        else:
            valor = costo
    elif estrategia == 'Greedy':
        if id == 0:
            valor = heuristica
        else:
            valor = heuristica
    elif estrategia == 'A':
        if id == 0:
            valor = heuristica
        else:
            valor = costo + heuristica
    else:
        valor = int(-9999)
        print("*********************ERROR*********************")
    return valor

def Calcularm1(estado):
    m1 = 500000000000000000
    for n in estado.NodosPorVisitar:
        for m in estado.NodosPorVisitar:
            if n < m:
                maux = math.sqrt(pow((float(ListaNodos[n].x)-float(ListaNodos[m].x)), 2) + pow((float(ListaNodos[n].y)-float(ListaNodos[m].y)), 2))
                if maux < m1:
                    m1 = maux
    return m1

def HeuristicaEuclidea(estado, m1):
    m2 = 500000000000000000
    for v in estado.NodosPorVisitar:
            maux = math.sqrt(pow((float(ListaNodos[int(estado.Localizacion)].x)-float(ListaNodos[v].x)), 2) + pow((float(ListaNodos[int(estado.Localizacion)].y)-float(ListaNodos[v].y)), 2))
            if maux < m2:
                m2 = maux
    m = min(m1, m2)*len(estado.NodosPorVisitar)
    return m

def HeuristicaArco(estado, min_long):
    return min_long*len(estado.NodosPorVisitar) 

def AlgoritmoBusqueda (e0, estrategia, ProfundidadMax):
    f.write("---------------------------\n")
    f.write("Estrategia "+ estrategia+"\n")
    f.write("---------------------------\n")
    
    print("---------------------------")
    print("Estrategia "+ estrategia)
    print("---------------------------")

    v = Visitados()
    frontera = PriorityQueue()
    Solucion = False
    ##HEURISTICA ARCO
    if Heuristica == "Arco":
        min_long = DiccionarioAristas["min_long"] #Minima longitud de la arista
        heuristica = HeuristicaArco(e0, min_long) 
    ##HEURISTICA EUCLIDEA
    elif Heuristica == "Euclidea":
        m1 = Calcularm1(e0) #Minima distancia de la lista de nodos por visitar
        heuristica = HeuristicaEuclidea(e0, m1)
    id = 0
    valor = valorEstrategia(estrategia, id, 0, 0, heuristica)
    n = NodoBusqueda(id, None, e0, valor, 0, 0, heuristica, None)
    frontera.put(n)
    id = id+1

    while Solucion==False and frontera.empty()==False:
        n = frontera.get()
        if CargarProblema.FuncionObjetivo(n.estado) ==True:
            Solucion = True
            if estrategia == "Greedy" or estrategia == "A":
                n.valor = n.valor - n.heuristica
                n.heuristica = 0
        else:
            if (v.Pertenece(n.getEstado())) == False and n.getProfundidad()<ProfundidadMax:
                v.Insercion(n.getEstado())
                for sucesor in n.getEstado().FuncionSucesor():
                    if Heuristica == "Arco":
                        heuristica = HeuristicaArco(sucesor.estadoAdy, min_long) ##Heuristica Arco
                    if Heuristica == "Euclidea":
                        heuristica = HeuristicaEuclidea(sucesor.estadoAdy, m1) ##Heuristica Euclidea
                    valor = valorEstrategia(estrategia, id, n.getProfundidad()+1, float(n.getCosto())+float(sucesor.costo), heuristica)
                    nh = NodoBusqueda(id, n, sucesor.estadoAdy, valor, n.getProfundidad()+1, float(n.getCosto())+float(sucesor.costo), heuristica, sucesor.accion)
                    frontera.put(nh)
                    id = id + 1
    if Solucion == True:
        caminoVacio = []
        camino = n.camino(n, caminoVacio)
        for i in range(len(camino)-1, -1, -1):
            print(camino[i].print())
            f.write(camino[i].print()+"\n")
    else:
        print("NO HAY SOLUCION")


def imprimirSolucion(estado, ProfMax):
    if Heuristica != "Arco" and Heuristica != "Euclidea":
        print("Error en el nombre definido de la heuristica")
        return 0
    f.write("=======================================\n")
    f.write("Estado inicial: "+ estado.print()+"\n")
    f.write("=======================================\n")

    print("=======================================")
    print("Estado inicial: "+ estado.print())
    print("=======================================")
    
    AlgoritmoBusqueda(estado, "A", ProfMax)
    AlgoritmoBusqueda(estado, "Uniform", ProfMax)
    AlgoritmoBusqueda(estado, "Greedy", ProfMax)
    AlgoritmoBusqueda(estado, "Breadth", ProfMax)
    #AlgoritmoBusqueda(estado, "Depth", ProfMax)
    
    #ESTRATEGIAS:
        #estrategia = "A" #A*
        #estrategia = "Uniform" #Coste Uniforme
        #estrategia = "Greedy" #Voraz
        #estrategia = "Breadth" #Anchura
        #estrategia = "Depth" #Profundidad


#---------------MAIN----------------
f = open ("Resultado.txt", 'a')
#HEURISTICAS:
Heuristica = "Arco"
#Heuristica = "Euclidea"

ProfMax = 400
e0 = CargarProblema.Estado(337,[249,431,1076])
imprimirSolucion(e0, ProfMax)

