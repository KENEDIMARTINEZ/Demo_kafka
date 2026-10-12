# Demo Kafka: registro de citas

Organización para dos integrantes, limitada a la versión V2 (Kafka) del trabajo. El PDF describe un trabajo más amplio; aquí adaptamos únicamente su sesión de Kafka y sus pruebas.

## Reparto de trabajo

| Responsable | Implementa | Entregable | Revisa |
| --- | --- | --- | --- |
| Tú (A) | Docker Compose, topic `citas`, productor y medición del envío confirmado | Entorno reproducible y `v2_kafka/productor.py` | Cambios de B |
| Tu compañero (B) | Consumidor de notificaciones, grupo de auditoría y registro de resultados | `v2_kafka/consumidor.py`, capturas y resultados | Cambios de A |
| Ambos | Integración, cuatro pruebas y explicación de la demo | Demo ejecutada en tu computadora | README y conclusiones |

Los archivos Python son tareas pendientes: esta entrega deja la organización y la infraestructura base.

## Orden de trabajo

1. **Sesión 1 (juntos, 45–60 min):** dar acceso al repositorio, clonar, levantar Kafka en tu máquina y comprobar las tres particiones.
2. **Sesión 2:** A desarrolla el productor; B desarrolla el consumidor. Si comparten la misma computadora, trabajan por turnos. Antes de empezar, ambos respetan el contrato descrito abajo.
3. **Sesión 3 (juntos, 60–90 min):** integrar por pull request; enviar 30 citas, probar 1, 3 y 4 consumidores, y demostrar auditoría.
4. **Sesión 4 (juntos, 60–90 min):** ejecutar las cuatro pruebas con tres repeticiones, guardar evidencia y grabar la demo.

Acuerden las fechas según su entrega. Al terminar cada sesión, anoten qué quedó listo y qué falta en el issue correspondiente.

## Contrato entre productor y consumidor

- Topic: `citas`, tres particiones y factor de replicación 1.
- Evento JSON: `{"id": 1, "paciente": "Paciente 1"}`. Usar datos ficticios.
- Clave del evento: `str(id)`. El orden se interpreta dentro de cada partición.
- Productor propuesto: `py v2_kafka/productor.py 30`.
- Consumidor propuesto: `py v2_kafka/consumidor.py notificaciones`.
- Auditoría propuesta: `py v2_kafka/consumidor.py auditoria-rep1`.
- Notificaciones simula 3 segundos de trabajo por evento. Auditoría lee sin esa demora.
- Confirmar el offset después de procesar; desactivar el commit automático. Una interrupción puede ocasionar reprocesamiento: no afirmar entrega exactamente una vez.
- `auto.offset.reset=earliest` permite comenzar desde el historial retenido cuando el grupo no tiene un offset válido. En cada repetición de auditoría usen un nombre nuevo.
- Medir la latencia hasta la confirmación del broker, mediante callback/flush y comprobación de errores; medir solo `produce()` refleja encolado local.

## Estructura acordada

```text
Demo_kafka/
  compose.yaml
  README.md
  .github/pull_request_template.md
  docs/organizacion.md
  v2_kafka/                      # productor.py y consumidor.py por implementar
  resultados/
    capturas/
    especificaciones_maquinas.md
```

## Levantar el entorno base

Requisitos: Docker Desktop funcionando con contenedores Linux y Git. Para la siguiente etapa de scripts, Python 3.10+ y el cliente `confluent-kafka`; acuerden y fijen la versión del cliente al integrar el código.

Desde la carpeta del repositorio, en PowerShell:

```powershell
docker compose config --quiet
docker compose pull
docker compose up -d --wait
docker compose ps
docker compose exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:19092 --describe --topic citas
```

Se crean Kafka y el topic `citas` automáticamente. El panel visual del anexo queda como ampliación opcional; los comandos permiten verificar las particiones desde el inicio.

Conexiones: los futuros scripts ejecutados en Windows usarán `localhost:9094`; aplicaciones dentro de la red Compose usarán `kafka:19092`. Se publica el puerto 9094 porque otro contenedor local (`kafka-citas`) ocupa el 9092. Dentro del contenedor, el listener externo sigue usando 9092.

Para apagar conservando los eventos:

```powershell
docker compose down
```

El volumen conserva los datos entre reinicios. Usen grupos nuevos para repetir las lecturas sin borrar el historial. Es un entorno local de un broker, sin tolerancia a la pérdida de ese broker.

## Trabajar con GitHub

Repositorio: https://github.com/KENEDIMARTINEZ/Demo_kafka

El propietario invita a su compañero desde **Settings → Collaborators → Add people**. El compañero acepta la invitación. Si editará código desde otro equipo, puede clonarlo sin instalar Docker. Si comparten tu computadora, usen la carpeta existente. Para un equipo adicional:

```powershell
git clone https://github.com/KENEDIMARTINEZ/Demo_kafka.git
cd Demo_kafka
```

Antes de crear una rama, consulten `git remote show origin` para identificar la rama principal. En los comandos siguientes se supone que se llama `main`; sustitúyanla si tiene otro nombre.

Cada tarea comienza con una rama propia:

```powershell
git switch main
git pull --ff-only origin main
git switch -c feat/productor-citas
```

A usa `feat/productor-citas`; B usa `feat/consumidor-citas`. Para tareas posteriores creen ramas nuevas, por ejemplo `docs/evidencias-kafka`.

Después de modificar y comprobar sus archivos:

```powershell
git status
git add v2_kafka/productor.py
git commit -m "Agrega productor de citas"
git push -u origin feat/productor-citas
```

B adapta la ruta, el mensaje y la rama al consumidor. En GitHub abran **Pull request** hacia la rama principal; el otro integrante revisa y reproduce el cambio antes de fusionar. No suban entornos virtuales, credenciales ni datos internos de Kafka. Kafka, su volumen y todos los mensajes estarán únicamente en tu máquina. GitHub comparte código y evidencias; ambos revisan y prueban los cambios en tu computadora.

La lista de issues y el protocolo de pruebas están en [docs/organizacion.md](docs/organizacion.md).

## Fuentes de trabajo

- Plan facilitado por el equipo: secciones 5.3–5.5 y anexos A–C. Se conserva `apache/kafka:4.2.0` para seguir su base.
- [Documentación oficial de Docker para Kafka](https://kafka.apache.org/42/getting-started/docker/).

## Estado

Base de organización preparada. Las pruebas de la aplicación y los resultados se completan cuando ambos implementen productor y consumidor; no hay mediciones inventadas.
