# labyrinth_game/utils.py
from . import constants as c


def describe_current_room(game_state: dict[str, list[str] | str | bool | int]) -> None:
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
    if c.ROOMS[game_state['current_room']]['puzzle']:
        print(c.ROOMS[game_state['current_room']]['puzzle'][0])
        answer = input("Ваш ответ: ").strip().lower()
        if answer == c.ROOMS[game_state['current_room']]['puzzle'][1]:
            print("Вы решили загадку!")
            c.ROOMS[game_state['current_room']]['puzzle'] = None
            # <-- Тут надо добавить какую-то награду
        else:
            print("Неверно. Попробуйте снова (solve).")
    else:
        print("Загадок здесь нет.")

def attempt_open_treasure(game_state: dict[str, list[str] | str | bool | int]) -> None:
    if "treasure chest" not in c.ROOMS[game_state['current_room']]['items']:
        print("Сундук уже открыт или отсутствует.")
        return

    if "treasure key" in game_state['player_inventory'] \
       or "rusty key" in game_state['player_inventory']:
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

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")