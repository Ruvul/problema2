import logging
from concurrent import futures
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
import requests
import threading

import grpc
import balance_pb2
import balance_pb2_grpc
import os

i=0

def RoundRobin():
    servers=['localhost:50052','localhost:50050','localhost:50049'] #sv1 sv2, sv3
    global i
    if i==0:
        port=servers[0]
        i+=1
        return port
    elif i==1:
        port = servers[1]
        i += 1
        return port
    elif i==2:
        port = servers[2]
        i = 0
        return port

class Balance(balance_pb2_grpc.BalanceServicer):

    def Create(self, request, context):
        nombre_f = request.nombre
        ruta_f = request.ruta

        #puerto = 'localhost:50052'
        puerto=RoundRobin()

        with grpc.insecure_channel(puerto) as channel:
            stub2 = balance_pb2_grpc.BalanceStub(channel)
            respuesta = stub2.Create2(balance_pb2.SolicitudCreate2(nombre=nombre_f, ruta=ruta_f))
        return balance_pb2.RespuestaCreate(conf=respuesta.conf)

    def Read(self, request, context):
        nombre_f = request.nombre
        ruta_f = request.ruta
        puerto=RoundRobin()

        with grpc.insecure_channel(puerto) as channel:
            stub2 = balance_pb2_grpc.BalanceStub(channel)

            for respuesta in stub2.Read2(balance_pb2.SolicitudRead2(nombre=nombre_f, ruta=ruta_f)):
                print(respuesta.contenido)
                yield balance_pb2.RespuestaRead(contenido=respuesta.contenido)

    def Write(self, request, context):
        nombre_f = request.nombre
        ruta_f = request.ruta

        puerto=RoundRobin()

        with grpc.insecure_channel(puerto) as channel:
            stub2 = balance_pb2_grpc.BalanceStub(channel)
            respuesta = stub2.Write2(balance_pb2.SolicitudWrite2(nombre=nombre_f, contenido=request.contenido,ruta=ruta_f))

        return balance_pb2.RespuestaWrite(conf=respuesta.conf)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    balance_pb2_grpc.add_BalanceServicer_to_server(Balance(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()