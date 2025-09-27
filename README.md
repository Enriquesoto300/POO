# Fokemon — Resumen del código y uso de POO

## Fokemon es un juego de consola escrito en Python. Incluye:  





- Mapa ASCII navegable con WASD.

- Exploración y eventos aleatorios.

- Combates por turnos contra Fokemon salvajes.

- Guardado/carga de partidas en JSON.

- Sistema de movimientos con variantes (doble, pierde turno, sin efecto).

- Todos los Fokemon son subclases de una clase base Fokemon   

**El código está pensado como ejemplo práctico de programación orientada a objetos aplicada a un pequeño juego.**  

## __Estructura principal (qué archivos / funciones mirar).__
- Movimiento — clase que modela un movimiento/ataque. (definición cerca de inicio)

- Fokemon — clase base (padre) de todos los Fokemon. (inmediatamente después)

- Subclases Fokelava, Fokeagua, Fokehoja, etc. — cada una hereda de Fokemon y define stats y movimientos.

- WILD_POKEMON_FACTORIES y create_random_wild() — fábrica para crear instancias de Fokemon salvajes.

- Partida — clase que guarda el estado del jugador, equipo, mapa, historial y guarda/carga en JSON.

- render_map, move_player, check_for_event — lógica del mapa y la exploración.

- combate — bucle de combate por turnos.

- main y menu_principal — punto de entrada y menús.

## Conceptos de POO usados y dónde están en el código.



**1. Clases** 
- Movimiento y Fokemon son las clases principales.

- Movimiento agrupa nombre, poder, tipo y variante; su método atacar() encapsula la lógica de cálculo de daño.

- Fokemon agrupa atributos (nombre, tipo, hp, stats, movimientos) y comportamientos (atacar, heal_full, is_fainted).

- Las clases Fokelava, Fokeagua, Fokehoja, etc. son subclases que heredan de Fokemon.

Ubicación en el código: ver las definiciones de class Movimiento: y class Fokemon: y las clases concretas que siguen.









**2. Objetos e instancias**
- Cada vez que llamas Fokelava(), Fokeagua() o Movimiento(...) estás creando instancias de clases (objetos) que contienen su propio estado (HP, movimientos, etc.).

- El equipo del jugador (partida.team) es una lista de instancias Fokemon.

- Los enemigos salvajes creados por create_random_wild() son también instancias de subclases de Fokemon.

Ejemplos prácticos: en elegir_starter() se crean 10 starters; en create_random_wild() se crea un salvaje.


**3. Herencia**
- Todas las clases concretas (Fokelava, Fokeagua, ...) hacen class Fokelava(Fokemon): ... y usan super().__init__(...) para reutilizar la inicialización base.

- Gracias a la herencia no hay que repetir los métodos comunes (por ejemplo atacar, is_fainted, heal_full) en cada clase.

Dónde mirar: definiciones de cada class Foke....

**4. Polimorfismo**

Polimorfismo = "tratar objetos de diferentes subclases de la misma forma".

- En combate(...) y en la función create_random_wild(), cualquier instancia devuelta (sea Fokelava o Fokeagua) se usa de la misma manera: llamamos wild.atacar(...), wild.is_fainted() o wild.movimientos. El bucle de combate no necesita saber la clase concreta del rival.

- Movimiento.atacar(self, atacante, defensor) opera con cualquier atacante y defensor que implementen los atributos esperados (ataque, defensa, tipo, hp), por lo que cualquier Fokemon puede llamar al método sin importar su subclase.

Ejemplo: en el bucle, p.atacar(sel_idx, wild) funciona igual si wild es de cualquier clase de Fokemon.

**5. Encapsulación**
- Cada clase agrupa datos y comportamientos relacionados: Movimiento encapsula todo lo necesario para aplicar un ataque; Fokemon encapsula estado y acciones de una criatura.

- Aunque los atributos son públicos por simplicidad (self.hp, self.ataque), están agrupados y accesibles sólo a través de métodos (por ejemplo atacar, heal_full) durante el flujo normal del juego. Esto facilita mantener y controlar la modificación del estado.

**6. Composición**

- Fokemon contiene una lista de objetos Movimiento. Es un ejemplo claro de composición (un Fokemon está formado por movimientos).

- Partida contiene objetos Fokemon (equipo) y un diccionario map_icons, historial, etc.

Dónde mirar: en Fokemon.__init__ (movimientos) y Partida.__init__ (team, map_icons).

**7. Responsabilidad única (Single Responsibility)**

- Movimiento — solo calcula y describe ataques.

- Fokemon — modela una criatura (stats, movimientos, acciones básicas).

- Partida — administra estado de la partida (posiciones, guardado/carga, historial).

- combate y render_map — funcionan como controladores de las reglas del juego y la UI de consola.

Esto facilita cambiar o extender una parte sin tocar las demás.

**8. Serialización y reconstrucción de objetos (guardar/cargar)**

- Partida.save() convierte el estado a JSON (listas/diccionarios) y lo escribe a disco.

- _poke_to_dict() serializa un Fokemon (incluye el nombre de la clase en "class").

- _dict_to_poke() intenta reconstruir la instancia llamando al constructor de la clase correspondiente en WILD_POKEMON_FACTORIES. Si no la encuentra, construye una instancia genérica Fokemon.

- Esto demuestra cómo convertir objetos en datos simples y luego reconstruirlos, un patrón común en juegos y aplicaciones.

Dónde mirar: métodos save, load, _poke_to_dict, _dict_to_poke de la clase Partida.

## Flujo de ejecución
**1. main() muestra el menu_principal() (crear/cargar/salir).**

**2. Si creas partida, elegir_starter() crea una instancia Fokemon y Partida la guarda en partida.team.**

**3. En el bucle principal se muestra render_map(partida) y se espera entrada WASD u otras teclas.**

**4. Moverse puede disparar check_for_event(). Si hay evento, se crea un Fokemon salvaje mediante create_random_wild() y se llama a combate(partida, wild).**

**5. combate() ejecuta el bucle por turnos usando los métodos atacar() de los objetos Fokemon y Movimiento.**

**6. Resultado del combate (victoria/derrota/huida) se guarda en partida.history y se persiste con partida.save().**
## Guía Práctica para Ejecutar el Juego
#### Si es la primera vez que usas un proyecto de Python, sigue estos pasos:

**1. Instalar Python**

- Descarga e instala Python 3.10 o superior.

- Asegúrate de marcar la opción "Add Python to PATH" durante la instalación.

**2. Descargar el código**

- Descarga el archivo 

```Fokemon_game.py``` o clona el repositorio desde GitHub:

```git clone https://github.com/Enriquesoto300/POO.git```

```cd POO```

**3. Ejecutar el juego**

- Abre una terminal en la carpeta del proyecto y escribe:

```python Fokemon_game.py ```

**4. Jugar**
- Selecciona Nueva Partida y elige tu Fokemon inicial.

- Usa las teclas W, A, S, D para moverte en el mapa.

- Cuando encuentres un Fokemon salvaje, entra en combate.

- Desde el Menú (tecla M) puedes ver tu equipo, guardar la partida y regresar al menú principal.

- Si cierras el juego, podrás cargar tu partida después desde la opción Cargar Partida.

## Conclusión
**1. Clases y Subclases**

- La clase Fokemon es la clase padre, que representa el modelo genérico de cualquier Fokemon.

- Todas las demás clases como Fokelava, Fokeagua, Fokehoja, etc., son subclases que heredan de Fokemon.

- Gracias a esta herencia, cada subclase puede reutilizar código común y, si lo necesita, añadir su propia lógica (por ejemplo, sus propios ataques).

**2. Objetos e Instancias**

- Cada vez que el jugador o el sistema crea un Fokemon, en realidad está creando una instancia de una clase.

- Esto permite que cada Fokemon tenga propiedades únicas (HP, ataques, posición en el mapa) pero siga el mismo modelo general.

**3. Atributos**

- Los atributos como hp, ataque, defensa, tipo, arte_ascii son propiedades encapsuladas dentro de cada objeto.

- Así se logra que cada Fokemon tenga estadísticas propias que no afectan a otros Fokemon.

**4. Herencia**

- Todas las subclases de Fokemon heredan sus métodos (atacar, heal_full, is_fainted) sin necesidad de reescribirlos.

- Esto reduce la duplicación de código y hace más fácil agregar nuevos Fokemones en el futuro.

**5. Polimorfismo**

- La función create_random_wild() devuelve un Fokemon sin importar qué clase específica sea.

- De la misma manera, el sistema de combate funciona para cualquier Fokemon, ya que todos tienen los mismos métodos (atacar, is_fainted).

- Esto es polimorfismo: distintos objetos respondiendo a las mismas llamadas de método de manera coherente.

En conclusión, para este proyecto se abordaron todos los temas solicitados por el docente, aunque en lo personal considero que se sintió todo un poco apresurado (lo sé, tuvimos muchísimo tiempo para hacerlo), pero me han parecido conceptos bastante interesantes. Al principio parecía un paradigma relativamente sencillo, pero creo que la dificultad fue progresando significativamente (No es queja) hasta llegar al punto de necesitar solicitar la ayuda de la IA, aún así, una mayor dificultad también implica una mayor necesidad de estudiar, lo que inevitablemente conlleva a aprender sí o sí todo el tema. Este es un ejemplo completo de POO, mostrando cómo usar clases, subclases, objetos, atributos, herencia y polimorfismo en un contexto real.
