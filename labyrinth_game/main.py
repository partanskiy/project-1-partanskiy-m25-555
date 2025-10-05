#!/usr/bin/env python3
from . import player_actions as pa
from . import utils as u

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0,  # Количество шагов
}

def main():
    """Основная функция игры - запускает игровой цикл."""
    print("Добро пожаловать в Лабиринт сокровищ!")
    u.describe_current_room(game_state)
    while not game_state['game_over']:
        command = pa.get_input("\nВведите команду: ")
        process_command(game_state, command)

def process_command(game_state: dict[str, list[str] | str | bool | int],
                    command: str) -> None:
    """Обрабатывает команды игрока и выполняет соответствующие действия."""
    if command in ["north", "south", "east", "west"]:
        command = "go " + command
    command, *args = command.split()
    match command:
        case "help":
            u.show_help(args)
        case "look":
            u.describe_current_room(game_state)
        case "use":
            pa.use_item(game_state, " ".join(args))
        case "go":
            pa.move_player(game_state, " ".join(args))
        case "take":
            pa.take_item(game_state, " ".join(args))
        case "inventory":
            pa.show_inventory(game_state)
        case "solve":
            if game_state['current_room'] == "treasure_room":
                u.attempt_open_treasure(game_state)
            else:
                u.solve_puzzle(game_state)
        case "use treasure chest":
            u.attempt_open_treasure(game_state)
        case "quit" | "exit":
            game_state['game_over'] = True
            print("Вы вышли из игры.")

if __name__ == "__main__":
    main()
