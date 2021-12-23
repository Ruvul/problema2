from __future__ import print_function

import logging

import grpc
import balance_pb2
import balance_pb2_grpc

def Crear(stub,ruta):
    print("CREATE:")
    name = input("Inserte el nombre del archivo a crear: ")
    respuesta=stub.Create(balance_pb2.SolicitudCreate(nombre=name,ruta=ruta))
    print("Respuesta recibida: " + respuesta.conf)

def Leer(stub,ruta):
    print("READ:")
    name = input("Inserte el nombre del archivo a leer: ")
    #respuesta=stub.Read(usuarios_pb2.SolicitudRead(nombre=name,ruta=ruta))
    #cont=respuesta.contenido
    print("Respuesta recibida. Contenido del archivo:")
    print("")
    for respuesta in stub.Read(balance_pb2.SolicitudRead(nombre=name,ruta=ruta)):
        print(respuesta.contenido)
    print("Archivo leido correctamente!")
    #print(cont)

def Escribir(stub,ruta):
    print("WRITE:")
    name = input("Inserte el nombre del archivo a editar: ")
    cont= input("Inserte el contenido del archivo: ")
    respuesta = stub.Write(balance_pb2.SolicitudWrite(nombre=name, contenido=cont,ruta=ruta))
    print("Respuesta recibida: " + respuesta.conf)

def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = balance_pb2_grpc.BalanceStub(channel)
        ruta="C:/Users/Allan/Desktop/Redes 2/prob2"
        print(ruta)

        while True:
            op = int(input("0: CREATE | 1: READ | 2: WRITE: "))

            if op==0:
                Crear(stub,ruta)
            elif op==1:
                Leer(stub,ruta)
            elif op==2:
                Escribir(stub,ruta)
            else:
                print("Entrada invalida...")



if __name__ == '__main__':
    logging.basicConfig()
    run()