import heapq
import random

import simpy


class Evento:
    def __init__(self, tiempo, tipo, cliente):
        # Representa un evento en el sistema, como la llegada o salida de un cliente.
        self.tiempo = tiempo
        self.tipo = tipo  # Puede ser "llegada" o "salida"
        self.cliente = cliente  # Cliente asociado al evento

    def __lt__(self, other):
        # Sobrecarga del operador < para comparar eventos por tiempo.
        return self.tiempo < other.tiempo


class Cliente:
    def __init__(self, llegada, atencion):
        # Representa a un cliente con su tiempo de llegada y tiempo de atención.
        self.llegada = llegada  # Tiempo de llegada del cliente
        self.atencion = atencion  # Tiempo de atención requerido para el cliente


class Tienda:
    def __init__(self, env, capacidad_servidores, tasa_llegada_media, tiempo_atencion_media):
        # Representa la tienda que modela el sistema de colas con servidores finitos.
        self.env = env
        self.servidores = simpy.Resource(env, capacity=capacidad_servidores)
        self.tasa_llegada_media = tasa_llegada_media
        self.tiempo_atencion_media = tiempo_atencion_media
        self.cola_espera = []  # Cola de espera para los clientes
        self.eventos = []  # Lista de eventos programados
        self.tiempo_espera_total = 0  # Acumulador para el tiempo total de espera
        self.num_clientes_atendidos = 0  # Contador de clientes atendidos
        self.tiempo_max_espera = 0  # Almacena el tiempo máximo de espera
        self.longitud_cola_total = 0  # Contador para la longitud total de la cola
        self.eventos_atendidos = []  # Lista para almacenar eventos de clientes atendidos

    def llegada_cliente(self, cliente):
        # Maneja la llegada de un cliente al sistema.
        heapq.heappush(self.cola_espera, cliente)
        evento_salida = Evento(cliente.llegada + cliente.atencion, "salida", cliente)
        heapq.heappush(self.eventos, evento_salida)

    def atender_cliente(self, cliente):
        # Maneja la atención de un cliente por parte de un servidor.
        self.num_clientes_atendidos += 1
        tiempo_espera = self.env.now - cliente.llegada
        self.tiempo_espera_total += tiempo_espera
        self.tiempo_max_espera = max(self.tiempo_max_espera, tiempo_espera)
        evento_atendido = Evento(self.env.now, "atendido", cliente)
        self.eventos_atendidos.append(evento_atendido)

    def simular(self, tiempo_simulacion):
        # Función principal para simular el sistema de colas.
        while self.env.now < tiempo_simulacion:
            if not self.cola_espera or self.env.now < self.cola_espera[0].llegada:
                # Generar nuevo cliente si no hay cola o la cola está vacía
                tiempo_llegada = self.env.now + random.expovariate(1 / self.tasa_llegada_media)
                tiempo_atencion = random.expovariate(1 / self.tiempo_atencion_media)
                cliente = Cliente(tiempo_llegada, tiempo_atencion)
                evento_llegada = Evento(tiempo_llegada, "llegada", cliente)
                heapq.heappush(self.eventos, evento_llegada)
            evento = heapq.heappop(self.eventos)
            self.env.run(until=evento.tiempo)
            if evento.tipo == "llegada":
                self.llegada_cliente(evento.cliente)
            elif evento.tipo == "salida":
                cliente_atendido = heapq.heappop(self.cola_espera)
                self.atender_cliente(cliente_atendido)
            elif evento.tipo == "atendido":
                # No hacemos nada especial, solo registramos el evento atendido
                pass
            self.longitud_cola_total += len(
                self.cola_espera
            )  # Añadimos la longitud actual de la cola al contador
