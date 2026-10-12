# Organización de la parte Kafka

## Issues por crear en GitHub

Copien cada fila como un issue y asignen su responsable. Muevan su estado entre Pendiente, En curso, En revisión y Terminado en GitHub Projects, o usen etiquetas equivalentes.

| Issue | Responsable | Depende de | Criterio para cerrar |
| --- | --- | --- | --- |
| 1. Validar entorno Docker en tu PC | A, con B | Ninguno | Kafka saludable y topic con 3 particiones en tu máquina |
| 2. Implementar productor de citas | A | 1 | Envía la cantidad solicitada, comprueba confirmación y errores del broker, imprime tiempos |
| 3. Implementar consumidor y auditoría | B | 1 | Grupo configurable, demora para notificaciones, offset confirmado al final y cierre limpio |
| 4. Integrar y demostrar particiones | Ambos | 2 y 3 | 30 eventos procesados; se observa asignación con 1, 3 y 4 consumidores del mismo grupo |
| 5. Registrar pruebas y capturas | B, con A | 4 | Cuatro pruebas, tres repeticiones cada una, condiciones y observaciones registradas |
| 6. Preparar explicación y video | Ambos | 5 | README reproducible, evidencia de replay y video breve de respaldo |

## Reglas de colaboración

1. Una tarea por rama y por pull request. El otro integrante revisa.
2. A mantiene Compose y productor; B mantiene consumidor y evidencias. Si necesitan editar el mismo archivo, coordinen primero en el issue.
3. Antes de fusionar, indicar comandos ejecutados, resultado y captura cuando corresponda.
4. Al fusionarse un cambio, actualizar la rama principal con `git pull --ff-only` antes de iniciar otra tarea. Si comparten la carpeta, terminen y guarden los cambios antes de cambiar de rama; no trabajen simultáneamente en ramas distintas dentro de esa carpeta.
5. Cada integrante ejecuta la demo completa y debe explicar topic, partición, grupo, offset y replay.

## Pruebas V2 pendientes

| Prueba | Procedimiento | Registrar |
| --- | --- | --- |
| 1. Latencia de registro | Consumidor activo, enviar 10 citas | Tiempo por envío confirmado, promedio y errores |
| 2. Consumidor apagado | Apagar consumidores, enviar 10 citas confirmadas y volver a iniciarlos | IDs enviados/procesados, faltantes y duplicados |
| 3. Paralelismo | Enviar 30 citas con 1 consumidor y luego otro lote con 3; esperar asignación antes de enviar | Tiempo desde el primer envío hasta terminar el lote, particiones por consumidor |
| 4. Replay | Procesar un lote y abrir un grupo de auditoría nuevo | Número e IDs de eventos históricos releídos |

Hacer tres repeticiones de cada prueba. Registrar CPU, RAM, sistema operativo, versión de Docker y commit utilizado. Para comparar repeticiones de paralelismo, consumir primero cualquier pendiente y evitar contar eventos de lotes anteriores. Un grupo nuevo puede leer todo el historial retenido, no solo el último lote: distinguir los IDs de cada lote y el total histórico esperado.

Para evidencias, usar nombres como `p3_v2_rep2_A.png` en `resultados/capturas/`. Los tiempos dependen de la asignación de claves a particiones; no asumir reparto exacto ni fijar los números esperados como resultados medidos.

Formato acordado para el futuro registro de resultados:

```text
prueba,version,repeticion,valor,unidad,maquina,responsable,observacion
```

## Guion de exposición

- A: explicar el escenario de citas, levantar Docker, mostrar topic y productor.
- B: mostrar consumidores, offsets y el cuarto consumidor sin partición asignada.
- Ambos: abrir auditoría con grupo nuevo, explicar por qué puede releer y comentar resultados medidos.

La implementación termina cuando ambos pueden ejecutar y explicar los pasos documentados en tu máquina, con sus evidencias guardadas. Solo tu computadora necesita Docker y Kafka; el compañero puede revisar y aportar código mediante GitHub. Este alcance cubre solo Kafka; el resto del trabajo general se integra por separado con el equipo.
