# labyrinth_game/player_actions.py
from . import constants as c
from . import utils as u


def show_inventory(game_state: dict[str, list[str] | str | bool | int]) -> None:
    if game_state['player_inventory']:
        item_str = ", ".join(game_state['player_inventory'])
        print(f"Инвентарь: {item_str}")
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> ") -> str:
    try:
        inp = input(prompt).strip().lower()
        return inp
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state: dict[str, list[str] | str | bool | int],
                direction: str) -> None:
    if direction in c.ROOMS[game_state['current_room']]['exits']:
        new_room = c.ROOMS[game_state['current_room']]['exits'][direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        u.describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state: dict[str, list[str] | str | bool | int],
              item_name: str) -> None:
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
            case "rusty key" | "treasure key":
                if "treasure chest" in c.ROOMS[game_state['current_room']]['items']:
                    print("Используйте этот ключ на сундуке с помощью solve")
                else:
                    print("Вы не можете использовать этот ключ пока что...")
            case _:
                print("Вы не знаете как использовать этот предмет.")
    else:
        print("У вас нет такого предмета.")