# Учёт серверов

Консольное приложение на Python для учёта серверов:

- Добавление, удаление, поиск
- Сохранение в JSON
- Бэкапы
- Автоматизация через bash и Docker
- Тестирование с `pytest`

## Функции

- ✅ Добавить/удалить сервер
- ✅ Поиск по IP, статусу
- ✅ Сохранение и бэкапы
- ✅ Bash-скрипт `run_server.sh`
- ✅ Docker-образ
- ✅ Тесты на `pytest`

## Как запустить

### 1. Локально

```bash
python servers.py
```

### 2. Через Docker

```
docker build -t servers-app .
docker run -it -v ${PWD}:/app servers-app
```

### Запуск тестов

```
pytest
pytest tests/test_servers.py::test_save_and_load -v -s
```
