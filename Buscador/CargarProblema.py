#!/usr/bin/python3

import CargarDatos
import hashlib

ListaNodos = CargarDatos.ListaNodos
DiccionarioAristas = CargarDatos.DiccionarioAristas

class Estado:
    IDEstado = ""
    Localizacion = ""
    NodosPorVisitar = []

    def setIDEstado(self, IDEstado):
        self.IDEstado = IDEstado
    def getIDEstado(self):
        return self.IDEstado

    def setLocalizacion(self, Localizacion):
        self.Localizacion = Localizacion
    def getLocalizacion(self):
        return self.Localizacion

    def __init__(self, Localizacion, NodosPorVisitar):
        self.IDEstado = self.crearID(Localizacion, NodosPorVisitar)
        self.Localizacion = Localizacion
        self.NodosPorVisitar = NodosPorVisitar
    
    def crearID(self, Localizacion, NodosPorVisitar):
        cadena = "("+str(Localizacion)+","+"["
        for i in NodosPorVisitar:
            cadena = cadena + str(i)
            if i != NodosPorVisitar[len(NodosPorVisitar)-1]:
                cadena = cadena + ","
        cadena = cadena + "])"
        md5_hash2 = hashlib.md5()
        md5_hash2.update(cadena.encode())
        return(md5_hash2.hexdigest())

    def FuncionSucesor(self):
        sucesoresEstado = []
        nodoVisitado = False
        indice = 0
        nuevosNodosPorVisitar = []
        for i in ListaNodos[int(self.getLocalizacion())].ListaAdyacencia:   
            nuevosNodosPorVisitar = self.NodosPorVisitar[:]
            if i in nuevosNodosPorVisitar:
                nuevosNodosPorVisitar.remove(i)
            
            nuevoEstado = Estado(str(i),nuevosNodosPorVisitar[:])
            accion = (str(self.getLocalizacion()),str(i))
            coste = DiccionarioAristas.get(accion)
            s = Sucesores(nuevoEstado, accion, coste)
            sucesoresEstado.append(s)
            
        return sucesoresEstado

    def print(self):
        cadena = "(" +str(self.getLocalizacion())+ ",["
        for i in self.NodosPorVisitar:
            cadena = cadena + str(i)
            if i != self.NodosPorVisitar[len(self.NodosPorVisitar)-1]:
                cadena = cadena + ","
        cadena= cadena +"])"
        return cadena


class Sucesores: 

    def __init__(self, estadoAdy, accion, costo):
        self.estadoAdy= estadoAdy
        self.accion = accion
        self.costo = costo

    def setestadoAdy(self, estadoAdy):
        self.estadoAdy = estadoAdy
    def getestadoAdy(self):
        return self.estadoAdy

    def setaccion(self, accion):
        self.accion = accion
    def getaccion(self):
        return self.accion

    def setcosto(self, costo):
        self.costo = costo
    def getcosto(self):
        return self.costo

    def print(self):
        cadena = "Accion: " +str(self.getaccion()[0])+ " -> " +str(self.getaccion()[1]) + " Estado nuevo (" + self.getestadoAdy().getLocalizacion() + "," + str(self.getestadoAdy().NodosPorVisitar)  +") || Coste: "+self.costo
        return cadena


def comprobarEstadoInicial(estadoInicial):
    for nodosPorVisitar in estadoInicial.NodosPorVisitar:
        if estadoInicial.getLocalizacion() == nodosPorVisitar:
            estadoInicial.NodosPorVisitar.remove(nodosPorVisitar)

def FuncionObjetivo(estado):
    finalizado = False
    if len(estado.NodosPorVisitar)==0:
        finalizado = True
    return finalizado