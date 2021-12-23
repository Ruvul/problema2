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

usuarios = ["Sofia", "Eduardo", "Juan"]
contra = "123"


class Balance(balance_pb2_grpc.BalanceServicer):
    """Missing associated documentation comment in .proto file."""

    def Balancear(self, request, context):
        new_ruta = request.puerto

        with grpc.insecure_channel(new_ruta) as channel:
            balance_pb2_grpc.BalanceStub(channel)

        return balance_pb2.RespuestaCreate(conf="Carga distribuida al servidor %s!" % new_ruta)

    def Create2(self, request, context):
        nombre_f = request.nombre
        ruta_f = request.ruta
        path = os.path.join(ruta_f, nombre_f)
        f = open(path, "wb")
        f.close()
        print("Sv3")
        return balance_pb2.RespuestaCreate2(conf="El archivo %s fue creado exitosamente!" % request.nombre)

    def Read2(self, request, context):
        nombre_f = request.nombre
        ruta_f = request.ruta
        path = os.path.join(ruta_f, nombre_f)
        f = open(path, "rb")
        t1 = f.readlines()
        print("Archivo leido correctamente!")
        f.close()
        t = []
        i = 0
        while i < t1.__len__():
            temp = t1[i].decode("utf-8")
            t.append(temp)
            i += 1
        # print(t)
        i = 0
        while i < t.__len__() - 1:
            t[i] = t[i].strip("\r\n")
            i += 1
        # print(t)
        for linea in t:
            texto = linea
            yield balance_pb2.RespuestaRead2(contenido=texto)

        print("Sv3")

    def Write2(self, request, context):
        nombre_f = request.nombre
        ruta_f = request.ruta
        # print(ruta_f)
        path = os.path.join(ruta_f, nombre_f)
        f = open(path, "w")
        f.write(request.contenido)
        f.close()
        # print("Archivo modificado correctamente!")
        print("Sv3")
        return balance_pb2.RespuestaWrite2(conf="Archivo modificado correctamente!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    balance_pb2_grpc.add_BalanceServicer_to_server(Balance(), server)
    server.add_insecure_port('[::]:50049')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()