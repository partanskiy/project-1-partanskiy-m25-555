# labyrinth_game/constants.py


# Игровые константы
EVENT_PROBABILITY = 10  # Вероятность случайного события (1 из 10)
EVENT_TYPE_COUNT = 3    # Количество типов случайных событий
STEP_INCREMENT = 1      # Инкремент шагов при перемещении

# Константы для ловушки
CRITICAL_DAMAGE_VALUE = 0     # Критическое значение damage (смерть)

# Константы для seed вычислений
TRAP_SEED_MULTIPLIER_WITH_ITEMS = 4    # Множитель для seed при наличии предметов
TRAP_SEED_MULTIPLIER_EMPTY = 3         # Множитель для seed при пустом инвентаре
TRAP_SEED_OFFSET = 42                  # Смещение для seed ловушки
EVENT_SEED_MULTIPLIER = 7              # Множитель для seed событий
EVENT_SEED_OFFSET = 1                  # Смещение для seed событий
EVENT_TYPE_SEED_MULTIPLIER_STEPS = 3   # Множитель шагов для seed типа события
EVENT_TYPE_SEED_MULTIPLIER_INVENTORY = 5  # Множитель инвентаря для seed типа события
EVENT_TYPE_SEED_OFFSET = 2             # Смещение для seed типа события

# Константы для форматирования
HELP_COMMAND_WIDTH = 16       # Ширина выравнивания команд в help

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение"
}

ROOMS: dict[str, str | dict[str, str] | list[str] | tuple[str, str] | None] = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта...',
        'exits': {'north': 'hall', 'east': 'trap_room',
                  'west': 'runic_sanctuary', 'south': 'mirror_chamber'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': ('Большой зал с эхом. По центру стоит небольшой пьедестал с '
                        'маленьким железным сундучком.'),
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': ['iron chest'],
        'puzzle': ('На пьедестале надпись: "Назовите число, которое идет '
                   'после девяти". Введите ответ числом или словом.', 
                   '10', 'десять')
    },
    'trap_room': {
          'description': ('Комната с хитрой плиточной поломкой. На стене видна '
                          'надпись: "Осторожно — ловушка".'),
          'exits': {'west': 'entrance'},
          'items': ['treasure key'],
          'puzzle': ('Система плит активна. Чтобы пройти, назовите слово "шаг" '
                     'три раза подряд (введите "шаг шаг шаг")', 'шаг шаг шаг')
    },
    'library': {
          'description': 'Пыльная библиотека. На полках старые свитки.',
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient book'],
          'puzzle': ('В одном свитке загадка: "Что растёт, когда ест, и '
                     'умирает, когда пьёт?" (ответ одно слово)', 
                     'огонь', 'пламя') 
    },
    'armory': {
          'description': ('Старая оружейная комната. На стене висит меч, рядом — '
                          'небольшая бронзовая шкатулка.'),
          'exits': {'south': 'library'},
          'items': ['sword', 'bronze box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': ('Комната, стены которой покрыты золотом и серебром. '
                          'На столе большой сундук. Он заперт.'),
          'exits': {'south': 'hall'},
          'items': ['treasure chest'],
          'puzzle': ('_', '10')
    },
    'mirror_chamber': {
          'description': ('Загадочная комната, полная зеркал всех форм и размеров. '
                          'Отражения создают бесконечные коридоры иллюзий. В центре - '
                          'светящийся кристалл.'),
          'exits': {'north': 'entrance', 'east': 'mirror_chamber',
                    'west': 'mirror_chamber', 'south': 'mirror_chamber'},
          'items': ['crystal orb', 'silver mirror'],
          'puzzle': ('Зеркала показывают загадку: "Я всегда с тобой, но никогда '
                     'не касаюсь. Показываю правду, но могу и солгать. Что я?" '
                     '(ответ одно слово)', 'отражение')
    },
    'runic_sanctuary': {
          'description': ('Древнее святилище с высокими каменными стенами, покрытыми '
                          'светящимися рунами. Воздух пропитан магической энергией. '
                          'На алтаре лежит древний артефакт.'),
          'exits': {'east': 'entrance'},
          'items': ['ancient rune', 'mystical staff', 'stone tablet'],
          'puzzle': ('Руны на стене складываются в загадку: "Что сильнее меча, но '
                     'не режет? Что ярче солнца, но не слепит?" (ответ одно слово)',
                     'знание', 'знания')
    }
}