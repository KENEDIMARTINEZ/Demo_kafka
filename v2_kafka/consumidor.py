import json
import os
import sys
import time
from confluent_kafka import Consumer

# Configuración del broker (por defecto 127.0.0.1:9094 según compose.yaml)
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9094")

# Grupo de consumidores (por defecto 'notificaciones' o el pasado por argumento, ej: 'auditoria')
grupo = sys.argv[1] if len(sys.argv) > 1 else "notificaciones"

consumidor = Consumer({
    "bootstrap.servers": bootstrap_servers,
    "group.id": grupo,               # Cada grupo lleva su propia posición/marcador (offset)
    "auto.offset.reset": "earliest", # Un grupo NUEVO empieza desde el primer evento disponible
    "enable.auto.commit": False,     # Commit manual tras procesar el mensaje
})

consumidor.subscribe(["citas"])
print(f"Grupo '{grupo}' [PID: {os.getpid()}] conectado a {bootstrap_servers}", flush=True)
print(f"Esperando eventos del topic 'citas'... (Ctrl+C para salir)\n", flush=True)

try:
    while True:
        msg = consumidor.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error en mensaje: {msg.error()}", flush=True)
            continue

        cita = json.loads(msg.value().decode("utf-8") if isinstance(msg.value(), bytes) else msg.value())

        # Si pertenece al grupo de notificaciones, simula el trabajo lento (3 segundos)
        # Si es de auditoría u otro grupo, procesa sin demora para relectura rápida (replay)
        if grupo == "notificaciones":
            time.sleep(3)

        print(
            f"{time.strftime('%H:%M:%S')} [{grupo} PID:{os.getpid()}] Cita {cita['id']} "
            f"(partición {msg.partition()}, offset {msg.offset()})",
            flush=True
        )

        # Confirmación manual del offset
        consumidor.commit(message=msg, asynchronous=False)

except KeyboardInterrupt:
    print(f"\nFinalizando consumidor [{grupo} PID:{os.getpid()}]...")
finally:
    consumidor.close()
