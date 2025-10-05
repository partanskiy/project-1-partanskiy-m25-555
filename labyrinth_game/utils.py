# labyrinth_game/utils.py
import math

from . import constants as c


def describe_current_room(game_state: dict[str, list[str] | str | bool | int]) -> None:
    """Выводит описание текущей комнаты, предметов, выходов и загадок."""
    print(f'\n== {game_state["current_room"].upper()} ==')
    print(c.ROOMS[game_state['current_room']]['description'])
    if c.ROOMS[game_state['current_room']]['items']:
        item_str = ", ".join(c.ROOMS[game_state['current_room']]['items'])
        print(f"Заметные предметы: {item_str}")
    if c.ROOMS[game_state['current_room']]['exits']:
        exit_str = ", ".join(c.ROOMS[game_state['current_room']]['exits'])
        print(f"Выходы: {exit_str}")
    if c.ROOMS[game_state['current_room']]['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state: dict[str, list[str] | str | bool | int]) -> None:
    """Позволяет игроку решить загадку в текущей комнате."""
    if c.ROOMS[game_state['current_room']]['puzzle']:
        print(c.ROOMS[game_state['current_room']]['puzzle'][0])
        answer = input("Ваш ответ: ").strip().lower()
        if answer in c.ROOMS[game_state['current_room']]['puzzle'][1:]:
            print("Вы решили загадку!")
            c.ROOMS[game_state['current_room']]['puzzle'] = None
            if game_state['current_room'] == 'hall':
                print("Вы нашли ключ!")
                game_state['player_inventory'].append("treasure key")
            elif game_state['current_room'] == 'library':
                print("Вы нашли ключ!")
                game_state['player_inventory'].append("rusty key")
        else:
            if game_state['current_room'] == 'trap_room':
                trigger_trap(game_state)
            else:
                print("Неверно. Попробуйте снова (solve).")
    else:
        print("Загадок здесь нет.")

def attempt_open_treasure(game_state: dict[str, list[str] | str | bool | int]) -> None:
    """Позволяет игроку попытаться открыть сундук с сокровищами."""
    if "treasure chest" not in c.ROOMS[game_state['current_room']]['items']:
        print("Сундук уже открыт или отсутствует.")
        return

    if "rusty key" in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        c.ROOMS[game_state['current_room']]['items'].remove("treasure chest")
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        if input("Сундук заперт. ... Ввести код? (да/нет): ").strip().lower() == "да":
            code = input('Введите код для сундука или "отступить": ').strip().lower()
            if code == c.ROOMS[game_state['current_room']]['puzzle'][1]:
                print("Вы ввели правильный код. Сундук открыт!")
                c.ROOMS[game_state['current_room']]['items'].remove("treasure chest")
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            elif code == "отступить":
                print("Вы отступаете от сундука.")
                return
            else:
                print("Неверный код. Попробуйте снова.")
        else:
            print("Вы отступаете от сундука.")
            return

def show_help(commands: list[str]):
    """Показывает справку по командам игры."""
    if commands:
        for command in commands:
            # Ищем команду, которая содержит данную подстроку
            found_command = None
            for cmd_key in c.COMMANDS:
                if command == cmd_key.split()[0]:
                    found_command = cmd_key
                    break
            
            if found_command:
                print(f"  {found_command:<{c.HELP_COMMAND_WIDTH}} — "
                      f"{c.COMMANDS[found_command]}")
            else:
                print(f"  {command:<{c.HELP_COMMAND_WIDTH}} — неизвестная команда")
    else:
        print("\nВсе доступные команды:")
        for command, description in c.COMMANDS.items():
            print(f"  {command:<{c.HELP_COMMAND_WIDTH}} — {description}")

def pseudo_random(seed: float, modulo: int) -> int:
    """Генерирует псевдослучайное число на основе синусоидальной функции."""
    x = 0.5 * (math.sin(seed * 12.3456789) + 1) * 10000
    return int(x % modulo)

def trigger_trap(game_state: dict[str, list[str] | str | bool | int]) -> None:
    """Активирует ловушку, которая может убить игрока или удалить предмет."""
    print("Ловушка активирована! Пол стал дрожать...")
    if game_state['player_inventory'] != []:
        seed = (game_state['steps_taken'] * c.TRAP_SEED_MULTIPLIER_WITH_ITEMS + 
                len(game_state['player_inventory']))
        delete_item_index = pseudo_random(seed, len(game_state['player_inventory']))
        deleted_item = game_state['player_inventory'].pop(delete_item_index)
        print(f"Вы потеряли {deleted_item}.")
    else:
        seed = (game_state['steps_taken'] * c.TRAP_SEED_MULTIPLIER_EMPTY + 
                c.TRAP_SEED_OFFSET)
        damage = pseudo_random(seed, c.EVENT_TYPE_COUNT)
        if damage == c.CRITICAL_DAMAGE_VALUE:
            print("Неудачно упав, вы умерли...")
            game_state['game_over'] = True
        else:
            print("К счастью, вы пережили удар.")
        return

def random_event(game_state: dict[str, list[str] | str | bool | int]) -> None:
    """Генерирует случайные события во время игры (монетки, существа, звуки ловушки)."""
    seed = (game_state['steps_taken'] + 
            len(game_state['player_inventory']) * c.EVENT_SEED_MULTIPLIER + 
            c.EVENT_SEED_OFFSET)
    event = pseudo_random(seed, c.EVENT_PROBABILITY)
    if event == 0:
        event_type_seed = (game_state['steps_taken'] * 
                           c.EVENT_TYPE_SEED_MULTIPLIER_STEPS + 
                           len(game_state['player_inventory']) * 
                           c.EVENT_TYPE_SEED_MULTIPLIER_INVENTORY + 
                           c.EVENT_TYPE_SEED_OFFSET)
        event_type = pseudo_random(event_type_seed, c.EVENT_TYPE_COUNT)
        if event_type == 0:
            if "coin" not in game_state['player_inventory']:
                print("Вы нашли монетку!")
                game_state['player_inventory'].append("coin")
            else:
                print("Вы нашли ещё одну монетку, которую решили оставить на месте.")
        elif event_type == 1:
            print("Вы слышите странный шорох...")
            if "sword" in game_state['player_inventory']:
                print("Вы заметили некоторое существо, "
                      "однако оно испугалось вас и убежало.")
            else:
                print("Вы заметили некоторое существо! "
                      "Вы напуганы, однако это существо, оценив вас, "
                      "великодушно решило вас отпустить.")
        elif event_type == 2:
            if ("torch" not in game_state['player_inventory'] and
                game_state['current_room'] == "trap_room"):
                trigger_trap(game_state)
            else:
                print("Вы слышите странные звуки... Видимо где-то в лабиринте "
                      "сработала ловушка.")