# Secuencia automática para Vigor VS1-14MT

El [plano Ladder gráfico](ladder-grafico-vigor.pdf) representa las **89 redes** del programa, con contactos, ramas, temporizadores y bobinas. Las salidas físicas están juntas en la última página.

`secuencia-vigor.txt` contiene el mismo programa en mnemónicos Vigor para reproducirlo en **Ladder Master S**, en el orden indicado. Cada bloque separado por una línea en blanco es una red. Las líneas precedidas por `#` son títulos para la lectura. La entrega incluye el plano gráfico y el texto fuente. Quedan pendientes el proyecto editable `.PVS`, la compilación en Ladder Master S y las pruebas con la CPU y la hidráulica reales.

## Entradas y salidas

| Dirección | Señal |
|---|---|
| X0 | B1, noyo dentro |
| X1 | B2, noyo fuera |
| X2 | B3, micro de expulsión atrás |
| X3 | Molde abierto |
| X4 | Pulso de permiso para expulsar, procedente de la máquina |
| X5 | Pulso de orden de expulsión atrás, procedente de la máquina |
| Y0 | K3, noyo salir |
| Y1 | K4, noyo entrar |
| Y2 | K5, expulsión entrar |
| Y3 | K6, expulsión salir |
| Y4 | K8, habilitar presión |
| Y5 | Sexta salida, permiso de cierre hacia la inyectora |

El micro de expulsión atrás también llega a la inyectora por su circuito propio. La lógica parte de las señales activas a nivel alto en el PLC y del esquema corregido, con las ramas automáticas de K3.1 a K6.1 en Auto. Verificar el orden real de los bornes y la asignación de los relés en banco. X6 y X7 quedan disponibles.

## Pasos del ciclo y de la hidráulica

| Paso | Orden activa | Confirmación para avanzar |
|---|---|---|
| M10 | Espera sin movimiento | Molde abierto, noyo y expulsión dentro y nuevo flanco de X4 |
| M11 | K3 y K8 | X1 confirma noyo fuera y X0 se libera |
| M12 | K6 y K8 durante el avance. K6 se mantiene después de descargar K8 | X2 se ha liberado y llega el flanco de X5 tras la recogida |
| M13 | K4 y K8 | X0 confirma noyo dentro y X1 se libera. La expulsión sigue adelantada |
| M14 | K5 y K8 | X2 confirma expulsión atrás, con el noyo todavía dentro |
| M15 | Y5, con los dos micros dentro | Se detecta molde dejando de estar abierto y, después, nueva apertura |

X4 y X5 son pulsos de aproximadamente un segundo. El programa memoriza su efecto al cambiar de paso. Acepta X4 con el molde abierto y la base confirmada. Acepta X5 durante el avance o la espera de recogida, cuando X2 ya se ha liberado. Arrancar o salir de un fallo exige una nueva orden. El cierre se habilita después de completar la secuencia, permanece durante la pérdida normal de X3 al cerrar y se retira en la reapertura. La máquina conserva la comprobación del micro de expulsión atrás en su propia lógica. Verificar estos tiempos de intercambio con la interfaz real.

En la espera del robot, se mantiene K6 hasta recibir X5. El temporizador de avance descarga K8 sin asignar una posición de expulsión fuera. La posición durante esta fase depende del circuito hidráulico. Confirmar que se mantiene al descargar y que la presión de K8 puede habilitarse en el mismo scan que la válvula de movimiento. El programa aplica una sola orden de movimiento por paso. Verificar también la conmutación y el tiempo de liberación físicos de los relés entre pasos.

## Configuración inicial y diagnóstico

Los temporizadores T0 a T5 usan unidades de **100 ms**. Los registros son retentivos. Configurarlos con tiempos medidos en la instalación, con D7006 en 0, y verificar su contenido en el editor. Todos los tiempos deben ser positivos y se exige **D7001 < D7005 < D7002**. Los valores del simulador son datos artificiales y quedan en memoria del simulador. El fuente no carga tiempos a la CPU.

| Registro | Temporizador y función |
|---|---|
| D7000 | T0, tiempo máximo para confirmar noyo fuera |
| D7001 | T1, tiempo máximo para que se libere X2 al avanzar la expulsión |
| D7002 | T2, tiempo máximo desde ordenar expulsión fuera hasta recibir X5 |
| D7003 | T3, tiempo máximo para confirmar noyo dentro |
| D7004 | T4, tiempo máximo para confirmar expulsión atrás |
| D7005 | T5, duración de K8 durante el avance de expulsión antes de descargar a tanque |
| D7006 | Habilitación de puesta en marcha. **0 bloquea las salidas**. El programa exige **1** y tiempos válidos para mover |

**M90** enclava el fallo. **M91** indica finales del noyo contradictorios. **M92** indica pérdida de una confirmación requerida o retorno fuera de secuencia. **M93** indica X5 prematura. **M94** indica tiempo excedido. **M95** indica pérdida de configuración o habilitación durante el ciclo. **M50** indica configuración habilitada y válida. **M99** admite una orden de rearme de mantenimiento, con ambos mecanismos ya en base y X4 y X5 en reposo. El rearme vuelve a espera y requiere un nuevo X4 para moverse.

## Prueba y puesta en marcha

1. Reproducir las redes y compilar para la CPU exacta en Ladder Master S. Revisar contactos, bobinas y la base de tiempo de los temporizadores.
2. Probar la secuencia con el accionamiento hidráulico aislado. Confirmar salidas y pérdida de permiso ante falta de micro, pulsos prematuros, cambio de modo, pérdida de alimentación y tiempos excedidos. El Auto depende del mando externo del cuadro. Verificar que la rama de modo aísla las maniobras en Manual y que el cambio de modo obliga a empezar en espera. Si el PLC continúa alimentado fuera de Auto, revisar la indicación de modo disponible antes de habilitar el programa.
3. Confirmar en el circuito real qué hacen las válvulas al quitar tensión, la retención durante la recogida, los tiempos de presión y el comportamiento del permiso de cierre. Mantener resguardos, emergencia y protecciones de cierre bajo la cadena original de seguridad. Y5 es un permiso de proceso. La recuperación mecánica tras una parada se realiza por el procedimiento de la instalación.

`python simular_secuencia.py` ejecuta las redes del archivo de texto con entradas y reloj simulados. Requiere Python 3.10 o posterior y usa solo la biblioteca estándar. Las pruebas cubren el ciclo y la reapertura, pulsos, pérdida de sensores, tiempos excedidos, rearme y descarga de K8. La simulación verifica el orden lógico de bits.

[Manual de programación Vigor VS](https://www.vigorplc.com/v_comm/inc/download_file.asp?fid=36739&re_id=2853) · [Ladder Master S](https://www.vigorplc.com/en/download-c5052/Programming-Software-for-VS-VBS-Series.html) · [ISO 20430, seguridad en máquinas de inyección](https://www.iso.org/standard/68000.html)
