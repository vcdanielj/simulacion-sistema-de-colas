import random

import simpy

import matplotlib.pyplot
matplotlib.use("Agg")

#La clase cliente genera clientes con 3 parámetros, env, que seria el entorno que controla el tiempo
# en que ocurren las acciones, nombre que sera el nombre del cliente, y servidor que sera el
# servidor que atienda al cliente
# En el método visita, se guarda primero el momento de llegada del cliente, luego, se solicita un
# servidor para ser atendido, el "yield request" detiene la ejecución mientras se este
# atendiendo a un cliente, "espera" calcula lo que tardo el cliente en ser atendido
# y tiempo_servicio calcula el tiempo que duro el servicio, en una distribución normal



class Cliente:
    def __init__(self, env, nombre, servidor, tiempo_llegada):
        self.env = env
        self.nombre = nombre
        self.servidor = servidor
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_atencion = None

    def visita(self):
        # Momento de llegada a la cola
        llegada = self.tiempo_llegada
        yield self.env.timeout(self.tiempo_llegada)
        print(f"[{self.nombre}] Llegó a la cola en {self.env.now:.2f} minutos")
        with self.servidor.request() as request:
            yield request
            atendido = self.env.now - llegada
            self.tiempo_atencion = atendido
            print(f"[{self.nombre}] Está siendo atendido después de {atendido:.2f} minutos de espera")
            print(" ")
            tiempo_servicio = random.normalvariate(10, 3)
            yield self.env.timeout(tiempo_servicio)
            # Momento de salida del servidor
            print(f"[{self.nombre}] Salió del servidor en {self.env.now:.2f} minutos")
            print(" ")

class Simulacion:
    def __init__(self):
        # Inicializamos el entorno de simPy
        self.env = simpy.Environment()
        self.servidor = simpy.Resource(self.env, capacity=1)
    
    # Método que ejecuta la simulación de los clientes con tiempo de llegada y nombre de cliente.
    def ejecutar_simulacion(self, num_clientes):
        tiempos_llegada = sorted([random.expovariate(1.0) for _ in range(num_clientes)])  # Generar tiempos de llegada aleatorios y ordenarlos
        clientes=[]
        for i in range(num_clientes):
            cliente = Cliente(self.env, f'Cliente-{i+1}', self.servidor, tiempos_llegada[i])
            self.env.process(cliente.visita())
            clientes.append(cliente)
        self.env.run()
        return  clientes

'''
Por hacer => • Calcular el tiempo Promedio de espera, de llegada y de atencion de los clientes en forma de métrica :P
'''

