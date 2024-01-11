import simpy  # noqa: I001
from flask import Flask, jsonify, render_template

from utils import Tienda
from simulacion import Simulacion
app = Flask(__name__)


sim = Simulacion()

# Configuración de parámetros para la simulación
capacidad_servidores = 2
tiempo_simulacion = 480  # 8 horas en minutos
tasa_llegada_media = 10  # Clientes por minuto en promedio
tiempo_atencion_media = 5  # Tiempo promedio de atención por cliente en minutos

# Configuración del entorno de simulación
env = simpy.Environment()
tienda = Tienda(env, capacidad_servidores, tasa_llegada_media, tiempo_atencion_media)


@app.route("/")
def home():
    return render_template("/home.html")


@app.route("/colas-con-servidores-finitos")
def exercise5():
    return render_template("/exercise5.html")


@app.route("/colas-con-tiempos-de-servicio-variables")
def exercise6():
    return render_template("/exercise6.html")


@app.route("/datos")
def obtener_datos():
    datos_clientes=sim.ejecutar_simulacion(5)
    detalles_clientes = [
        {
            "tiempo_atencion": cliente.tiempo_llegada,
            "tiempo_espera": cliente.tiempo_atencion,
        }
        for cliente in datos_clientes
    ]

    datos = {
        "tiempo_promedio_espera": 1,
        "longitud_promedio_cola": 1,
        "tiempo_maximo_espera": 1,
        "detalles_clientes": detalles_clientes,
    }
    print(datos)
    return jsonify(datos)

@app.route("/simular")
def simular():
    tienda.simular(tiempo_simulacion)
    return "Simulación completada"


@app.route("/metricas")
def obtener_metricas():
    tiempo_promedio_espera = tienda.tiempo_espera_total / tienda.num_clientes_atendidos
    longitud_promedio_cola = tienda.longitud_cola_total / tiempo_simulacion
    tiempo_maximo_espera = tienda.tiempo_max_espera

    detalles_clientes = [
        {
            "tiempo_atencion": evento.tiempo,
            "tiempo_espera": evento.tiempo - evento.cliente.llegada,
        }
        for evento in tienda.eventos_atendidos
    ]

    metricas = {
        "tiempo_promedio_espera": tiempo_promedio_espera,
        "longitud_promedio_cola": longitud_promedio_cola,
        "tiempo_maximo_espera": tiempo_maximo_espera,
        "detalles_clientes": detalles_clientes,
    }

    return jsonify(metricas)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
