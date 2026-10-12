import json
import os
import sys
import time
from confluent_kafka import Producer

# Configuración del broker (por defecto 127.0.0.1:9094 según compose.yaml)
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9094")

# Número de citas a registrar (por defecto 10, o el argumento pasado por CLI)
n = next((int(a) for a in sys.argv[1:] if a.isdigit()), 10)

productor = Producer({"bootstrap.servers": bootstrap_servers})

print(f"Iniciando productor conectado a {bootstrap_servers}...")
print(f"Enviando {n} citas al topic 'citas'...\n")

for i in range(1, n + 1):
    inicio = time.time()
    cita = {"id": i, "paciente": f"Paciente {i}"}
    
    # La clave (id) determina la partición (hashing consistente) y garantiza el orden dentro de la partición
    productor.produce("citas", key=str(i), value=json.dumps(cita))
    productor.poll(0)
    print(f"{time.strftime('%H:%M:%S')} Cita {i} registrada en {time.time() - inicio:.3f} s", flush=True)

# Asegura que todos los mensajes en cola se envíen y confirmen antes de terminar
productor.flush()
print(f"\nEnvío de {n} citas finalizado exitosamente.", flush=True)
