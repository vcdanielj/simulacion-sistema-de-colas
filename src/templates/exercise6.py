import simpy
import random

#La clase cliente genera clientes con 3 parámetros, env, que seria el entorno que controla el tiempo
# en que ocurren las acciones, nombre que sera el nombre del cliente, y servidor que sera el
# servidor que atienda al cliente
# En el método visita, se guarda primero el momento de llegada del cliente, luego, se solicita un
# servidor para ser atendido, el "yield request" detiene la ejecución mientras se este
# atendiendo a un cliente, "espera" calcula lo que tardo el cliente en ser atendido
# y tiempo_servicio calcula el tiempo que duro el servicio, en una distribución normal

class Cliente:
    def __init__(self, env, nombre, servidor):
        self.env = env
        self.nombre = nombre
        self.servidor = servidor

    def visita(self):
        llegada = self.env.now
        print(f"{self.nombre} llegó a la cola en {llegada} mins")

        with self.servidor.request() as request:
            yield request

            espera = self.env.now - llegada
            print(f"{self.nombre} esperó {espera} mins")

            tiempo_servicio = random.normalvariate(10, 3)
            yield self.env.timeout(tiempo_servicio)
            print(f"{self.nombre} salió del servidor a los {self.env.now} mins")

class Simulacion:
    #to do :p falta hacer la simulacion y agregar una forma de llevar las estadísticas
    #de los clientes, cual es el tiempo promedio etc etc


