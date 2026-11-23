# Contexto del Hobbywing XR10 Pro G2 Elite y el Pro10

El objetivo en pista es que el Pro10 con motor **6.5T** salga con una entrega parecida a la de un **10.5T** en los primeros metros y después entregue el empuje del 6.5T. El segundo objetivo es diseñar una **app Android propia**, personalizable por el piloto, que pueda leer y programar el variador a través del OTA cuando se haya validado el protocolo. Los perfiles de este documento son propuestas de partida. Falta probarlos en el coche del piloto.

## Equipo y datos de partida

| Elemento | Dato |
|---|---|
| Chasis | **Pro10 Pan Car**, tracción trasera. Marca y modelo exactos pendientes. |
| Variador | **Hobbywing XeRun XR10 Pro G2 Elite**. La documentación usada corresponde al **G2**, distinto del G2S y del G3. |
| Motor | **6.5T rojo**, descrito por el piloto como «Facom Icon Torque». La familia **Fantom ICON** es una identificación probable. Falta confirmar la referencia grabada. |
| Avance mecánico | **30° de serie**, según el piloto. Se toma como punto fijo para las primeras pruebas. |
| Desarrollo | **FDR 4,00**. Ruedas traseras de **60–62 mm**. Equivale a **47,1–48,7 mm por vuelta de motor**, calculados como π × diámetro ÷ FDR. |
| Emisora | **Sanwa**. El piloto tenía **30% de expo de gas**. Aclaró que ese 30% correspondía al expo. En Sanwa el EPA puede llegar al 150%. |
| Batería | El perfil se preparó suponiendo **LiPo 2S**. Conviene confirmar el paquete instalado. |
| Programador y teléfono | **Hobbywing OTA Programmer**, con identificación **2021DP16214**, y móvil **Android**. El identificador corresponde al módulo de radio **HW6187**. Hobbywing lista el OTA **30850400** como accesorio compatible. |

[Manual del XR10 Pro G2 y G2 Elite](https://www.hobbywing.com/en/uploads/file/20221024/c7c899724ffc421cf90154a7960384a0.pdf) · [Ficha del G2 Elite](https://www.hobbywing.com/en/products/xerun-xr10-pro-g2166) · [Identificación del HW6187](https://fccid.io/2AIWP-HW6187/User-Manual/User-Manual-5627061) · [Fantom Racing](https://fantomracing.com/products/replacement-sensor-board-5mm-or-6mm)

## Perfil base completo para HW Link

| ID | Nombre del ajuste | Valor base | Efecto y ajuste en pista |
|---|---|---|---|
| 1A | Running Mode | Forward with Brake | Marcha adelante y freno. |
| 1B | Max. Reverse Force | 25% | Inactivo con el modo de 1A. Si se habilita la marcha atrás, un valor mayor da más fuerza. |
| 1C | Cutoff Voltage | Auto | En LiPo 2S, umbral de 6,6 V para el paquete. |
| 1D | ESC Thermal Protection | 105 °C | Umbral de corte del ESC. |
| 1E | Motor Thermal Protection | 105 °C | Umbral de corte según el sensor. Su lectura puede diferir con motores de otras marcas. Medir también la carcasa con termómetro externo. |
| 1F | BEC Voltage | Valor actual compatible | Si se parte de cero, 6,0 V si el servo y el receptor lo admiten. |
| 1G | Remote Off | Disabled | Apagado desde el botón del ESC. |
| 1H | Sensor Mode | Full Sensored | Utiliza el cable de sensor con el motor compatible. |
| 1I | Motor Rotation | CW o CCW actual | Elegir el sentido que hace avanzar el chasis. |
| 2A | Throttle Rate Control | **12** | Ajuste principal al abrir a fondo. **9** si patina o se cruza. **15** si tiene agarre y responde tarde. |
| 2B | Throttle Curve | Linear | Una curva por debajo de la diagonal al principio suaviza el gas parcial. |
| 2C | Neutral Range | 6% | Probar **4%** si el neutro es estable y se busca menos zona muerta, o **8%** si el neutro es inestable. |
| 2D | Coast | 0% | Subirlo prolonga la rodada al levantar. Requiere 3A a 0%. |
| 2E | PWM Drive Frequency | **8 kHz** | **4 kHz** da más mordiente. **12 kHz** suaviza más y puede calentar el ESC. |
| 2F | Softening Value | **15°** | Aumentarlo suaviza el gas parcial. Probar **18°** si es brusco o **12°** si queda apagado. |
| 2G | Softening Range | **35%** | Porcentaje del recorrido inicial de gas. **30%** acorta la zona suavizada y **40%** la amplía. |
| 3A | Drag Brake Force | 0% | Más porcentaje da más retención en neutro. |
| 3B | Max. Brake Force | **70%** | Probar **60%** si bloquea o descoloca la trasera, o **75%** si falta frenada. |
| 3C | Initial Brake Force | = Drag Brake (0%) | Más porcentaje da más mordiente al primer toque. |
| 3D | Brake Rate Control | **12** | Probar **10** si el freno entra de golpe o **15** si entra lento. |
| 3E | Brake Curve | Linear | Una curva por debajo de la diagonal al comienzo suaviza el freno inicial. |
| 3F | Brake Frequency | 1 kHz | Probar **2 kHz** para un tacto de frenada más suave. |
| 3G | Brake Control | Linear | Dosificable. Traditional da una frenada más fuerte. |
| 4A | Boost Timing | **0°** | Avance electrónico máximo del Boost. |
| 4B | Boost Timing Activation | RPM | El modo RPM usa revoluciones. Auto usa la orden de gas. |
| 4C | Boost Start RPM | 6.000 rpm | Inactivo con Boost a 0°. Subirlo retrasa el inicio. |
| 4D | Boost End RPM | 22.500 rpm | Inactivo con Boost a 0°. Subirlo retrasa las rpm a las que llega todo el Boost. |
| 5A | Turbo Timing | **0°** | Avance electrónico adicional al mantener gas a fondo. |
| 5B | Turbo Delay | 0,40 s | Inactivo con Turbo a 0°. Subirlo retrasa la entrada desde que se alcanza gas a fondo. |
| 5C | Turbo Increase Rate | 3°/0,1 s | Un valor mayor aplica más rápido el Turbo. |
| 5D | Turbo Decrease Rate | 3°/0,1 s | Un valor mayor retira más rápido el Turbo al levantar. |

[Hoja oficial de ajustes del G2](https://www.hobbywing.com/en/uploads/file/20220916/a6d4c553237ca9e889b9395bd7576bdf.pdf)

## Sanwa y pruebas en pista

- **Emisora para la primera tanda.** EPA-H 100%, EPA-B 100%, expo de gas 0%, trim y subtrim de gas 0, curva lineal, ABS desactivado y failsafe de gas en neutro o sin salida. Si cambian los puntos finales o el neutro, recalibrar el ESC en el orden **neutro, gas a fondo, freno a fondo**. Si el ESC ya está calibrado con los recorridos al 100% y solo cambia el expo, se puede conservar la calibración. El rango hasta 150% amplía el recorrido de la señal, útil para servos y mecanismos, y no aumenta la potencia máxima de un ESC calibrado al 100%. [Manual Sanwa M17S, pág. 33](https://sanwa-denshi.co.jp/rc/Manual/Transmitter/M17S_MANUAL.pdf)
- **Interpretación de la arrancada.** 2A actúa sobre la rapidez de respuesta al abrir gas. 2F y 2G suavizan el gas parcial y 2G se refiere al recorrido del gatillo. El G2 carece de un disparo por metros recorridos. Tampoco hay una equivalencia de aceleración calibrada entre 6.5T y 10.5T. Si se dispone de un 10.5T de referencia, comparar las salidas a **2 y 5 m** en las mismas condiciones, además del empuje en recta.
- **Protocolo de comparación.** Cambiar un ajuste por tanda, empezando por 2A. Usar un diámetro trasero y condiciones de batería y agarre comparables. Medir motor y ESC inmediatamente al parar. Si el gas parcial necesita más suavidad tras ajustar el ESC, se puede probar **10–15% de expo en el sentido que suaviza** según el modelo Sanwa. En una gráfica, la curva debe empezar por debajo de la diagonal y terminar en el 100%.

## Perfiles para asfalto seco

| Parámetro | Rubí | Cerdanyola | AMSA asfalto |
|---|---:|---:|---:|
| 2A Throttle Rate Control | **12** | **14** | **10** |
| 2E PWM Drive Frequency | 8 kHz | 8 kHz | 8 kHz |
| 2F Softening Value | 15° | 12° | 18° |
| 2G Softening Range | 35% | 30% | 40% |
| 3B Max. Brake Force | 70% | 70% | 65% |
| 3D Brake Rate Control | 12 | 12 | 10 |
| 4A y 5A Boost y Turbo | 0° y 0° | 0° y 0° | 0° y 0° |

Conservar los demás valores del perfil base. En Rubí, bajar 2A de **12 a 9** si patina al abrir a fondo. En Cerdanyola, reservar **14** para una trasera que traccione bien y volver a **12** si desliza. En AMSA, subir de **10 a 12** si la salida queda lenta con buen agarre. AMSA también tiene pista de moqueta. Comprobar el reglamento vigente de la categoría antes de usar avance electrónico en carrera. [Club RC Rubí](https://www.clubradiocontrolrubi.com/quienes-somos/) · [Cerdanyola ModelCar Dubà](https://amsatrinitat.com/index.php/2024/09/26/4o-prueba-campeonato-cataluna-pista-electrico/) · [Circuitos de AMSA](https://amsatrinitat.com/index.php/circuitos/)

## Ejemplos de avance con el motor a 30°

- **Boost por rpm.** Ejemplo del manual con **4A = 5°**, **4B = RPM**, inicio **10.000 rpm**, final **15.000 rpm** y Turbo a cero. El avance electrónico añadido es **0°** por debajo del umbral, **+1°** a 11.000 rpm, **+3°** a 13.000 rpm y **+5°** a partir de 15.000 rpm. Las referencias nominales con el motor a 30° son **30°, 31°, 33° y 35°**. Subir solo el inicio reduce el intervalo de rpm en el que entran esos grados.
- **Turbo retrasado.** Ejemplo separado con **Boost = 0°**, **5A = 3°**, retardo **0,40 s** y subida y bajada **3°/0,1 s**. La entrada empieza después de **0,40 s continuos a fondo** y llega a **+3°** alrededor de **0,50 s**, con referencia nominal de **33°**. Al levantar, esos 3° se retiran en alrededor de **0,10 s**. Si el Boost de +5° y el Turbo de +3° coincidieran completos, la suma nominal sería **38°**. Es una suma para interpretar el ejemplo, no una medición del avance efectivo ni un valor objetivo.
- **Primera tanda y consumo.** Empezar con ambos avances electrónicos a cero y con los 30° mecánicos. Más avance puede cambiar consumo y temperatura. Si se prueba el Turbo, hacerlo por separado tras comprobar las temperaturas y la referencia del motor. Los grados de Softening describen el ajuste del ESC y no permiten calcular el avance efectivo restándolos del avance mecánico.

[Manual oficial del G2, apartados Softening, Boost y Turbo](https://www.hobbywing.com/en/uploads/file/20221024/c7c899724ffc421cf90154a7960384a0.pdf)

## App Android propia

El piloto quiere decidir la interfaz y el flujo de programación. Cuando planteó la app propia todavía no había probado **HW Link V2**. La función buscada incluye **leer el estado real del variador, seleccionar un perfil, comparar los cambios, confirmar la escritura y verificar el resultado**. Los perfiles deberían poder guardarse y editarse sin conexión. Una app que solo muestra tablas cubre la consulta, pero deja pendiente el objetivo de programar el ESC directamente.

| Área | Estado y alcance |
|---|---|
| Conexión oficial | **HW Link V2** comunica el teléfono con el OTA por BLE y permite leer y configurar el XR10. El OTA se conecta al puerto dedicado del variador. El registro de datos depende del ESC y del firmware. |
| Conexión de una app propia | Android documenta las APIs BLE. Es viable desarrollar la interfaz en Kotlin y mantener separado el transporte BLE del almacenamiento de perfiles. En Android 12 o posterior deben contemplarse los permisos de dispositivos cercanos. |
| Contrato de datos del ESC | El manual del **HW6187** describe el puente BLE-serie, no los mensajes de configuración específicos del XR10. No se localizó en las fuentes revisadas un SDK público o una especificación validada para leer y escribir este modelo. |
| Implementación | **Investigación de viabilidad.** A fecha del traspaso no hay código Android ni una prueba de escritura realizada en el equipo del piloto. Quedan por confirmar el firmware del ESC y del OTA y los comandos que utiliza esa combinación. |

[HW Link V2 en Google Play](https://play.google.com/store/apps/details?id=com.hobbywing.hwlink2) · [Hobbywing OTA Programmer](https://www.hobbywing.com/en/products/ota-programmer23) · [Conexión BLE en Android](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server) · [Permisos Bluetooth](https://developer.android.com/develop/connectivity/bluetooth/bt-permissions)

### Próxima prueba de banco

1. Identificar firmware de ESC y OTA, leer la configuración con HW Link V2 y conservar una referencia de los valores iniciales. Buscar documentación del fabricante para el protocolo. Si hace falta investigarlo, Android permite registrar el tráfico Bluetooth de una sesión normal con la app oficial y el equipo propio. [Diagnóstico Bluetooth en Android](https://source.android.com/docs/core/connect/bluetooth/verifying_debugging)
2. Con el coche inmovilizado, validar primero **la lectura de 2A** en el prototipo frente a la lectura oficial. Después probar una escritura reversible si se conoce el comando. Por ejemplo, si 2A está en **12**, pasar a **13**, leer, reiniciar el ESC, releer y restaurar **12**. Si el valor inicial difiere, conservarlo y restaurarlo al final de la prueba.
3. Validar los parámetros de gas y freno en la misma combinación de firmware antes de aplicar perfiles completos. Considerar un perfil aplicado solo tras releer los valores. Si se interrumpe la conexión, volver a leer el estado antes de decidir qué cambios repetir.

## Fichas imprimibles y repositorio

El repositorio **`cronos880-lang/Codex_Varios`** contiene las dos fichas publicadas. Cada una ocupa media hoja DIN A4 al imprimir al 100%. La rama de trabajo es **`entrega-rc-pro10-pdf`** y los archivos están en **`RC/Pro10/`**. La publicación de las fichas confirma su disponibilidad, no una validación de rendimiento en pista.

- [Ficha completa del XR10 Pro G2 Elite](https://github.com/cronos880-lang/Codex_Varios/blob/entrega-rc-pro10-pdf/RC/Pro10/ficha-pro10-xr10-g2-elite.pdf?raw=true)
- [Ficha corta de Rubí, Cerdanyola y AMSA](https://github.com/cronos880-lang/Codex_Varios/blob/entrega-rc-pro10-pdf/RC/Pro10/perfiles-pro10-rubi-cerdanyola-amsa.pdf?raw=true)
