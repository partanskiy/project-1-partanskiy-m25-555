install:
	@poetry install

project:
	@poetry run project

build:
	@poetry build

publish:
	@poetry publish --dry-run

package-install:
	@python3 -m pip install dist/*.whl

lint:
	@poetry run ruff check .

demo:
	@asciinema play demo.cast

help:
	@echo "Доступные команды:"
	@echo "  install         - Установка зависимостей через poetry"
	@echo "  project         - Запуск игры"
	@echo "  build           - Сборка пакета"
	@echo "  publish         - Тестовая публикация пакета"
	@echo "  package-install - Установка собранного пакета"
	@echo "  lint            - Проверка кода линтером"
	@echo "  demo            - Воспроизведение демо-записи"
	@echo "  help            - Показать эту справку"