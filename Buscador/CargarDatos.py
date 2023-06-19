#!/usr/bin/python3

import xml.sax

class Nodo:

    def __init__(self, id):
        self.id = id
        self.ListaAdyacencia = []
        self.idosm = "?"
        self.lon = "0"
        self.lat = "0"
        self.x = "0"
        self.y = "0"
    def set_id(self, id):
        self.id = id
    def get_id(self):
        return self.id

    def set_idosm(self, idosm):
        self.idosm = idosm
    def get_idosm(self):
        return self.idosm

    def set_lon(self, lon):
        self.lon = lon
    def get_lon(self):
        return self.lon

    def set_lat(self, lat):
        self.lat = lat
    def get_lat(self):
        return self.lat

    def set_x(self, x):
        self.x = x
    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y
    def get_y(self):
        return self.y

    def anadir_adyacencia(self, adyacencia):
        self.ListaAdyacencia.append(adyacencia)

class Claves:
    def __init__(self):
        osmid_nodo = "?"
        Longitud_nodo = "?"
        Latitud_nodo = "?"
        Longitud_arista = "?"
        x_nodo ="?"
        y_nodo="?"
    def setosmid_nodo(self, osmid_nodo):
        self.osmid_nodo = osmid_nodo
    def getosmid_nodo(self):
        return self.osmid_nodo

    def setLongitud_nodo(self, Longitud_nodo):
        self.Longitud_nodo= Longitud_nodo
    def getLongitud_nodo(self):
        return self.Longitud_nodo

    def setLatitud_nodo(self, Latitud_nodo):
        self.Latitud_nodo = Latitud_nodo
    def getLatitud_nodo(self):
        return self.Latitud_nodo

    def setLongitud_arista(self, Longitud_arista):
        self.Longitud_arista = Longitud_arista
    def getLongitud_arista(self):
        return self.Longitud_arista

    def setx_nodo(self, x_nodo):
        self.x_nodo = x_nodo
    def getx_nodo(self):
        return self.x_nodo

    def sety_nodo(self, y_nodo):
        self.y_nodo = y_nodo
    def gety_nodo(self):
        return self.y_nodo

class Arista:
    def __init__(self, source, target, id):
        self.source = source
        self.target = target
        self.id = id
        lon = "?"
    
    def set_source(self, source):
        self.source = source
    def get_source(self):
        return self.source

    def set_target(self, target):
        self.target = target
    def get_target(self):
        return self.target
    
    def set_lon(self, lon):
        self.lon = lon
    def get_lon(self):
        return self.lon

class Dato:
    def __init__(self, key):
        self.key = key

    def set_key(self, key):
        self.key = key
    def get_key(self):
        return self.key

    def set_data(self, data):
        self.data = data
    def get_data(self):
        return self.data


class PeopleHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        global a
        self.current = name
        if name == "node":
            n2 = Nodo(attrs['id'])
            ListaNodos.append(n2)
        if name == "data":
            d = Dato(attrs['key'])
            ListaData.append(d)
        if name == "edge":
            a = Arista(attrs['source'], attrs['target'], attrs['id'])
        if name == "key":
            if attrs['for'] == "edge" and attrs['attr.name'] == "length" and attrs['attr.type'] == "string":
                c.setLongitud_arista(attrs['id'])
            if attrs['for'] == "node" and attrs['attr.name'] == "lat" and attrs['attr.type'] == "string":
                c.setLatitud_nodo(attrs['id'])
            if attrs['for'] == "node" and attrs['attr.name'] == "lon" and attrs['attr.type'] == "string":
                c.setLongitud_nodo(attrs['id'])
            if attrs['for'] == "node" and attrs['attr.name'] == "osmid_original" and attrs['attr.type'] == "string":
                c.setosmid_nodo(attrs['id'])
            if attrs['for'] == "node" and attrs['attr.name'] == "x" and attrs['attr.type'] == "string":
                c.setx_nodo(attrs['id'])
            if attrs['for'] == "node" and attrs['attr.name'] == "y" and attrs['attr.type'] == "string":
                c.sety_nodo(attrs['id'])


    
    def characters(self, content):
        if self.current == "node":
            self.node = content
        elif self.current == "data":
            self.data = content
        elif self.current == "edge":
            self.edge = content

    def endElement(self, name):
        global a
        global MenorHeuristica
        if name == "node":
            n1 = ListaNodos.pop()
            while len(ListaData):
                d = ListaData.pop()
                if d.get_key() == c.osmid_nodo:
                    n1.set_idosm(d.get_data())
                elif d.get_key() == c.Longitud_nodo:
                    n1.set_lon(d.get_data())
                elif d.get_key() == c.Latitud_nodo:
                    n1.set_lat(d.get_data())
                elif d.get_key() == c.x_nodo:
                    n1.set_x(d.get_data())
                elif d.get_key() == c.y_nodo:
                    n1.set_y(d.get_data())
            ListaNodos.append(n1)
        elif name == "data":
            d = ListaData.pop()
            if d.get_key()  == c.getosmid_nodo() or d.get_key() ==c.getLongitud_nodo() or d.get_key()  == c.getLatitud_nodo() or d.get_key()  == c.getLongitud_arista() or d.get_key()  == c.getx_nodo() or d.get_key()  == c.gety_nodo():
                d.set_data(self.data)
                ListaData.append(d)
        elif name == "edge":
            while len(ListaData):
                d = ListaData.pop()
                if d.get_key() == c.getLongitud_arista():
                    a.set_lon(d.get_data())
            if DiccionarioAristas.get((str(a.get_source()), str(a.get_target()))) == None:
                DiccionarioAristas[(a.get_source(), a.get_target())] = a.get_lon()
                ListaNodos[int(a.get_source())].anadir_adyacencia(int(a.get_target()))
                if float(a.get_lon()) < MenorHeuristica:
                    MenorHeuristica = float(a.get_lon())
                    DiccionarioAristas["min_long"] = MenorHeuristica
         
        self.current = ""

handler = PeopleHandler()
global a
global MenorHeuristica
MenorHeuristica = 50000000
c = Claves()
ListaNodos = []
ListaData = []
DiccionarioAristas = {}
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
#parser.parse('CR_Capital.graphML.xml')
parser.parse('nuevo.graphxml.xml')

for i in ListaNodos:
    i.ListaAdyacencia.sort()
