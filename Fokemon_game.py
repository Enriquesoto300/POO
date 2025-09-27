import random
import json
import os
import time
import sys
from copy import deepcopy

SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar(ms=800):
    time.sleep(ms/1000)


TYPES = ["fuego", "agua", "planta", "normal"]
EFFECTIVENESS = {
    ("fuego", "planta"): 2.0,
    ("fuego", "agua"): 0.5,
    ("agua", "fuego"): 2.0,
    ("agua", "planta"): 0.5,
    ("planta", "agua"): 2.0,
    ("planta", "fuego"): 0.5,
}
def get_effectiveness(att_type, def_type):
    return EFFECTIVENESS.get((att_type, def_type), 1.0)


class Movimiento:
    def __init__(self, nombre, poder, tipo, variante="basico"):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo
        self.variante = variante

    def atacar(self, atacante, defensor):
        if self.variante == "sin":
            desc = f"{atacante.nombre} usó {self.nombre}... ¡Sin efecto!"
            return desc, 0, False
        atk = atacante.ataque
        df = max(defensor.defensa, 1)
        stab = 1.5 if self.tipo == atacante.tipo else 1.0
        effectiveness = get_effectiveness(self.tipo, defensor.tipo)
        rand = random.uniform(0.85, 1.0)
        damage = int(self.poder * (atk/df) * effectiveness * stab * rand)
        if self.variante == "doble":
            damage *= 2
            desc = f"{atacante.nombre} usó {self.nombre} — ¡Golpe doble!"
            return desc, damage, False
        elif self.variante == "pierde_turno":
            desc = f"{atacante.nombre} usó {self.nombre} — pero queda exhausto y pierde el siguiente turno."
            return desc, damage, True
        else:
            desc = f"{atacante.nombre} usó {self.nombre}."
            if effectiveness > 1:
                desc += " ¡Es super efectivo!"
            elif effectiveness < 1:
                desc += " No es muy efectivo..."
            return desc, damage, False

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) pwr:{self.poder} var:{self.variante}"


class Fokemon:
    def __init__(self, nombre, tipo, arte_ascii, ataque, defensa, hp_max, habilidad, movimientos):
        self.nombre = nombre
        self.tipo = tipo
        self.arte_ascii = arte_ascii
        self.ataque = ataque
        self.defensa = defensa
        self.hp_max = hp_max
        self.hp = hp_max
        self.habilidad = habilidad
        self.movimientos = movimientos
        self.perdio_turno = False

    def atacar(self, mov_idx, objetivo):
        mov = self.movimientos[mov_idx]
        desc, dmg, pierde_turno = mov.atacar(self, objetivo)
        objetivo.hp = max(objetivo.hp - dmg, 0)
        if pierde_turno:
            self.perdio_turno = True
        return desc, dmg

    def heal_full(self):
        self.hp = self.hp_max

    def is_fainted(self):
        return self.hp <= 0

    def evolucionar(self):
        return False

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) HP:{self.hp}/{self.hp_max} Atk:{self.ataque} Def:{self.defensa}"


ARTES = {
    "fokelava": "🌋",
    "fokeagua": "💧",
    "fokehoja": "🌿",
    "fokenegro": "🐦‍⬛",
    "fokeflam": "❤️‍🔥",
    "fokerain": "🌧️",
    "fokeverde": "🍃",
    "fokefuego": "🔥",
    "fokewave": "💦",
    "fokeindio": "🌱"
}


class Fokelava(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Chispa", 8, "fuego"),
            Movimiento("Llama", 12, "fuego"),
            Movimiento("Brasa Doble", 6, "fuego", variante="doble"),
            Movimiento("Descanso Forzado", 10, "normal", variante="pierde_turno")
        ]
        super().__init__("Fokelava", "fuego", ARTES["fokelava"],
                         ataque=14, defensa=9, hp_max=random.randint(40,50),
                         habilidad="llama viva", movimientos=movs)

class Fokeflam(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Mordisco Ígneo", 13, "fuego"),
            Movimiento("Aullar", 0, "normal", variante="sin"),
            Movimiento("Furia Doble", 7, "fuego", variante="doble")
        ]
        super().__init__("Fokeflam", "fuego", ARTES["fokeflam"],
                         ataque=16, defensa=11, hp_max=random.randint(45,55),
                         habilidad="fuego feroz", movimientos=movs)

class Fokefuego(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Ascuas",10,"fuego"),
            Movimiento("Zarpazo",8,"normal"),
            Movimiento("Latigazo",12,"fuego")
        ]
        super().__init__("Fokefuego","fuego",ARTES["fokefuego"],13,10,random.randint(38,48),"espíritu ardiente",movs)

class Fokeagua(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Chorro",10,"agua"),
            Movimiento("Gota Doble",6,"agua",variante="doble"),
            Movimiento("Empapado",12,"agua")
        ]
        super().__init__("Fokeagua","agua",ARTES["fokeagua"],12,12,random.randint(42,52),"piel acuática",movs)

class Fokerain(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Rociada",8,"agua"),
            Movimiento("Oleada",14,"agua"),
            Movimiento("Baile Húmedo",0,"normal",variante="sin")
        ]
        super().__init__("Fokerain","agua",ARTES["fokerain"],11,13,random.randint(36,46),"salpicadura",movs)

class Fokewave(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Mordisco",9,"normal"),
            Movimiento("Chapuzón",12,"agua")
        ]
        super().__init__("Fokewave","agua",ARTES["fokewave"],12,10,random.randint(40,50),"flotador",movs)

class Fokehoja(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Hoja Larga",10,"planta"),
            Movimiento("Polen Doble",6,"planta",variante="doble"),
            Movimiento("Raiz",12,"planta")
        ]
        super().__init__("Fokehoja","planta",ARTES["fokehoja"],11,12,random.randint(38,48),"clorofila",movs)

class Fokeverde(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Espina",9,"planta"),
            Movimiento("Tormenta Verde",13,"planta"),
            Movimiento("Somnolencia",0,"normal",variante="pierde_turno")
        ]
        super().__init__("Fokeverde","planta",ARTES["fokeverde"],12,14,random.randint(44,54),"espinas defensivas",movs)

class Fokeindio(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Ladrido",8,"normal"),
            Movimiento("Brote",11,"planta")
        ]
        super().__init__("Fokeindio","planta",ARTES["fokeindio"],10,11,random.randint(36,46),"pastizal vivo",movs)

class Fokenegro(Fokemon):
    def __init__(self):
        movs = [
            Movimiento("Golpe",10,"normal"),
            Movimiento("Empujón",7,"normal")
        ]
        super().__init__("Fokenegro","normal",ARTES["fokenegro"],11,11,random.randint(40,50),"versátil",movimientos=movs)

WILD_POKEMON_FACTORIES = [
    Fokelava, Fokeflam, Fokefuego, Fokeagua, Fokerain, Fokewave,
    Fokehoja, Fokeverde, Fokeindio, Fokenegro
]

def create_random_wild():
    cls_ = random.choice(WILD_POKEMON_FACTORIES)
    return cls_()


class Partida:
    def __init__(self, player_name, starter: Fokemon):
        self.player_name = player_name
        self.team = [starter]
        self.map_size = 11
        self.player_pos = [self.map_size//2, self.map_size//2]
        self.history = []
        self.turns = 0
        self.map_icons = self._place_static_icons()
        self.filename = os.path.join(SAVE_DIR, f"{player_name}.txt")

    def _place_static_icons(self):
        icons = {}
        choices = ["🦕", "🦕", "🦕", "🦕"]
        for _ in range(9):
            x = random.randint(1, self.map_size-2)
            y = random.randint(1, self.map_size-2)
            icons[(x,y)] = random.choice(choices)
        return icons

    def save(self):
        data = {
            "player_name": self.player_name,
            "team": [self._poke_to_dict(p) for p in self.team],
            "map_size": self.map_size,
            "player_pos": self.player_pos,
            "history": self.history,
            "map_icons": [{"pos":pos, "icon":icon} for pos,icon in self.map_icons.items()],
            "turns": self.turns
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.player_name = data["player_name"]
            self.team = [self._dict_to_poke(d) for d in data["team"]]
            self.map_size = data.get("map_size", 11)
            self.player_pos = data.get("player_pos", [self.map_size//2, self.map_size//2])
            self.history = data.get("history", [])
            self.map_icons = {tuple(x["pos"]): x["icon"] for x in data.get("map_icons", [])}
            self.turns = data.get("turns", 0)
            return True
        return False

    def _poke_to_dict(self, p: Fokemon):
        return {
            "class": p.__class__.__name__,
            "nombre": p.nombre,
            "tipo": p.tipo,
            "arte_ascii": p.arte_ascii,
            "ataque": p.ataque,
            "defensa": p.defensa,
            "hp_max": p.hp_max,
            "hp": p.hp,
            "habilidad": p.habilidad,
            "movimientos": [{"nombre":m.nombre,"poder":m.poder,"tipo":m.tipo,"variante":m.variante} for m in p.movimientos]
        }

    def _dict_to_poke(self, d):
        movs = [Movimiento(m["nombre"], m["poder"], m["tipo"], m.get("variante","basico")) for m in d.get("movimientos",[])]
        for factory in WILD_POKEMON_FACTORIES:
            if factory().__class__.__name__ == d.get("class"):
                p = factory()
                p.hp = d.get("hp", p.hp)
                p.hp_max = d.get("hp_max", p.hp_max)
                return p
        p = Fokemon(d.get("nombre","Unknown"), d.get("tipo","normal"), d.get("arte_ascii","?"),
                    d.get("ataque",10), d.get("defensa",10), d.get("hp_max",40), d.get("habilidad",""), movs)
        p.hp = d.get("hp", p.hp)
        return p

    def add_history(self, record: dict):
        self.history.append(record)
        self.save()


def render_map(partida: Partida):
    size = partida.map_size
    px, py = partida.player_pos
    cls()
    print("╔" + "═"* (size*2-1) + "╗")
    for y in range(size):
        row = ""
        for x in range(size):
            if (x,y) == (px,py):
                row += "😎 "
            elif (x,y) in partida.map_icons:
                row += partida.map_icons[(x,y)] + " "
            else:
                row += ". "
        print("║" + row[:-1] + "║")
    print("╚" + "═"* (size*2-1) + "╝")
    print("| ↑ W | ↓ S | ← A | → D | M - Menú | V - Volver | H - Historial")
    print("> ", end="", flush=True)


def move_player(partida: Partida, dirc):
    x,y = partida.player_pos
    if dirc == 'w': y = max(0, y-1)
    if dirc == 's': y = min(partida.map_size-1, y+1)
    if dirc == 'a': x = max(0, x-1)
    if dirc == 'd': x = min(partida.map_size-1, x+1)
    partida.player_pos = [x,y]
    partida.turns += 1

def check_for_event(partida: Partida):
    pos = tuple(partida.player_pos)
    if pos in partida.map_icons:
        icon = partida.map_icons.pop(pos)
        return True, f"Tocaste a {icon} y apareció un Fokemon salvaje!"
    if random.random() < 0.12:
        return True, "¡Aparece un Fokemon salvaje de la nada!"
    return False, ""


def combate(partida: Partida, wild_pokemon: Fokemon):
    cls()
    player_poke = partida.team[0]
    wild = deepcopy(wild_pokemon)
    p = deepcopy(player_poke)
    print("¡Comienza el combate!")
    pausar(900)
    turno_player = True
    combate_record = {"oponente": wild.nombre, "resultado": None}
    while True:
        cls()
        print("=== TU FOKEMON ===")
        print(p.arte_ascii, p.nombre, f"HP: {p.hp}/{p.hp_max}")
        print("=== SALVAJE ===")
        print(wild.arte_ascii, wild.nombre, f"HP: {wild.hp}/{wild.hp_max}")
        print()
        if turno_player:
            if p.perdio_turno:
                print(f"{p.nombre} está exhausto y pierde su turno.")
                p.perdio_turno = False
                turno_player = False
                pausar(900)
                continue
            print("[1] Luchar  [2] Estado  [3] Huir")
            choice = input("Elige: ").strip()
            if choice == "2":
                print("--- ESTADO ---")
                print(p)
                input("Enter para continuar...")
                continue
            elif choice == "3":
                if random.random() > 0.5:
                    print("¡Huiste con éxito!")
                    combate_record["resultado"] = "Huida"
                    partida.add_history(combate_record)
                    return "huida"
                else:
                    print("¡No pudiste huir!")
                    turno_player = False
                    pausar(900)
                    continue
            else:
                print("Elige movimiento:")
                for i, m in enumerate(p.movimientos):
                    print(f"{i+1}. {m}")
                sel = input("Movimiento #> ").strip()
                try:
                    sel_idx = max(0, int(sel)-1)
                    if sel_idx >= len(p.movimientos): raise ValueError
                except:
                    print("Movimiento inválido.")
                    pausar(900)
                    continue
                desc, dmg = p.atacar(sel_idx, wild)
                print(desc)
                if dmg>0:
                    print(f"Infligiste {dmg} HP.")
                pausar(900)
                if wild.is_fainted():
                    print(f"¡Derrotaste a {wild.nombre}!")
                    combate_record["resultado"] = "Victoria"
                    partida.add_history(combate_record)
                    return "victoria"
                turno_player = False
        else:
            if wild.perdio_turno:
                print(f"{wild.nombre} está exhausto y pierde su turno.")
                wild.perdio_turno = False
                turno_player = True
                pausar(900)
                continue
            mov_idx = random.randint(0, len(wild.movimientos)-1)
            desc, dmg = wild.atacar(mov_idx, p)
            print(desc)
            if dmg>0:
                print(f"{wild.nombre} infligió {dmg} HP.")
            pausar(900)
            if p.is_fainted():
                print(f"¡Perdiste con {p.nombre}!")
                combate_record["resultado"] = "Derrota"
                partida.add_history(combate_record)
                return "derrota"
            turno_player = True


def menu_principal():
    cls()
    print(" FOKEMON GAME ")
    print("[1] Nueva Partida")
    print("[2] Cargar Partida")
    print("[3] Salir")
    choice = input("> ").strip()
    return choice

def elegir_starter():
    starters = [Fokelava(), Fokeagua(), Fokehoja(), Fokeflam(), Fokefuego(), Fokerain(), Fokewave(), Fokeverde(), Fokeindio(), Fokenegro()]
    print("Elige tu Fokemon inicial:")
    for i, s in enumerate(starters):
        print(f"[{i+1}] {s.nombre} {s.arte_ascii}")
    sel = input("> ").strip()
    try:
        sel_idx = max(0,int(sel)-1)
        if sel_idx >= len(starters): raise ValueError
        return starters[sel_idx]
    except:
        print("Selección inválida, se asignará aleatorio.")
        return random.choice(starters)

def main():
    while True:
        choice = menu_principal()
        if choice=="3": break
        elif choice=="1":
            name = input("Nombre del jugador: ").strip()
            starter = elegir_starter()
            partida = Partida(name, starter)
            print(f"¡Bienvenido {name}! Tu starter es {starter.nombre} {starter.arte_ascii}")
        elif choice=="2":
            name = input("Nombre del jugador a cargar: ").strip()
            partida = Partida(name, Fokelava())
            if not partida.load():
                print("No se encontró la partida.")
                pausar(1000)
                continue
        else:
            continue

        
        while True:
            render_map(partida)
            move = input().strip().lower()
            if move in ["w","a","s","d"]:
                move_player(partida, move)
                event, msg = check_for_event(partida)
                if event:
                    print(msg)
                    pausar(900)
                    wild = create_random_wild()
                    combate(partida, wild)
            elif move=="m":
                print("=== MENÚ ===")
                print("1. Ver equipo")
                print("2. Guardar partida")
                print("3. Salir al menú principal")
                sub = input("> ").strip()
                if sub=="1":
                    for p in partida.team:
                        print(p)
                    input("Enter para continuar...")
                elif sub=="2":
                    partida.save()
                    print("Partida guardada.")
                    pausar(900)
                elif sub=="3":
                    break
            elif move=="h":
                print("=== HISTORIAL ===")
                for h in partida.history[-10:]:
                    print(h)
                input("Enter para continuar...")
            elif move=="v":
                break

if __name__=="__main__":
    main()




