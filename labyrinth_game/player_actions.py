# labyrinth_game/player_actions.py
from . import constants as c
from . import utils as u


def show_inventory(game_state: dict[str, list[str] | str | bool | int]) -> None:
    """Показывает содержимое инвентаря игрока."""
    if game_state['player_inventory']:
        item_str = ", ".join(game_state['player_inventory'])
        print(f"Инвентарь: {item_str}")
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> ") -> str:
    """Получает ввод от пользователя с обработкой исключений."""
    try:
        inp = input(prompt).strip().lower()
        return inp
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state: dict[str, list[str] | str | bool | int],
                direction: str) -> None:
    """Перемещает игрока в указанном направлении с проверкой доступности выхода."""
    if direction in c.ROOMS[game_state['current_room']]['exits']:
        new_room = c.ROOMS[game_state['current_room']]['exits'][direction]
        if new_room == "treasure_room":
            if "treasure key" not in game_state['player_inventory']:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
            else:
                print("Вы используете найденный ключ, "
                      "чтобы открыть путь в комнату сокровищ.")
                game_state['player_inventory'].remove("treasure key")
        elif (game_state['current_room'] == "mirror_chamber" and
              new_room == "mirror_chamber"):
            print("Вы прошли сквозь зеркала, однако у вас не получилось выбраться.")
            return  # Не переходим в новую комнату и не увеличиваем шаги

        game_state['current_room'] = new_room
        game_state['steps_taken'] += c.STEP_INCREMENT
        u.describe_current_room(game_state)
        u.random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state: dict[str, list[str] | str | bool | int],
              item_name: str) -> None:
    """Позволяет игроку поднять предмет из текущей комнаты."""
    if item_name in c.ROOMS[game_state['current_room']]['items']:
        if c.ROOMS[game_state['current_room']]['puzzle'] is None:
            if item_name == "treasure chest":
                print("Вы не можете поднять сундук.")
                return
            if item_name not in game_state['player_inventory']:
                game_state['player_inventory'].append(item_name)
                print(f"Вы подняли: {item_name}.")
            else:
                print("Вы уже подняли этот предмет.")
            c.ROOMS[game_state['current_room']]['items'].remove(item_name)
        else:
            print("Вы не можете поднять этот предмет пока что... (solve)")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict[str, list[str] | str | bool | int],
             item_name: str) -> None:
    """Позволяет игроку использовать предмет из инвентаря."""
    if item_name in game_state['player_inventory']:
        match item_name:
            case "torch":
                print("В комнате стало светлее.")
            case "sword":
                print("Вы преисполнились силой и уверенностью.")
            case "iron chest":
                print("Вы открыли железный сундучок, но увидели лишь паутину в углу.")
            case "bronze box":
                print("Вы открыли бронзовый ящик и нашли ржавый ключ.")
                if "rusty key" not in game_state['player_inventory']:
                    game_state['player_inventory'].append("rusty key")
                game_state['player_inventory'].remove(item_name)
            case "rusty key":
                if "treasure chest" in c.ROOMS[game_state['current_room']]['items']:
                    print("Используйте этот ключ на сундуке с помощью solve")
                else:
                    print("Вы не можете использовать этот ключ пока что...")
            case "treasure key":
                print("Вы не можете использовать этот ключ пока что...")
            case "mystical staff":
                print("Магический посох светится теплым светом.")
            case _:
                print("Вы не знаете как использовать этот предмет.")
    else:
        print("У вас нет такого предмета.")
