import pytest
import os
import sys

sys.path.insert(0, '.')

from servers import is_valid_ip, add_server, servers, remove_server, load_servers, save_servers


# Очищаем список серверов перед каждым тестом
@pytest.fixture(autouse=True)
def clear_servers():
    servers.clear()


# Тест: валидация IP-адреса
def test_is_valid_ip():
    assert is_valid_ip("192.168.1.1") == True
    assert is_valid_ip("255.255.255.255") == True
    assert is_valid_ip("256.1.1.1") == False
    assert is_valid_ip("192.168.1") == False
    assert is_valid_ip("192.168.1.1.1") == False
    assert is_valid_ip("abc.def.ghi.jkl") == False


# Тест: добавление сервера
def test_add_server():
    # Имитируем ввод
    import builtins
    builtins.input = lambda _: "test-server" if "Имя" in _ else \
        "192.168.1.10" if "IP" in _ else \
            "web" if "Роль" in _ else \
                "online" if "Статус" in _ else \
                    "y"  # по умолчанию

    add_server()
    assert len(servers) == 1
    assert servers[0]["name"] == "test-server"
    assert servers[0]["ip"] == "192.168.1.10"
    assert servers[0]["role"] == "web"
    assert servers[0]["status"] == "online"
    assert servers[0]["cpu"] == 8  # значение по умолчанию
    assert servers[0]["ram"] == 16  # значение по умолчанию


# Тест: удаление сервера
def test_remove_server():
    # Добавим сервер вручную
    servers.append({"name": "to-remove", "ip": "1.1.1.1", "role": "db", "status": "online", "cpu": 4, "ram": 8})

    remove_server("to-remove")
    assert len(servers) == 0

    # Попробуем удалить несуществующий сервер
    remove_server("not-exists")  # не должно быть ошибки


# Тест: сохранение и загрузка
def test_save_and_load():
    # Добавим сервер
    servers.append({"name": "saved-server", "ip": "2.2.2.2", "role": "cache", "status": "offline", "cpu": 4, "ram": 4})

    # Сохраним
    save_servers()

    # Загрузим
    load_servers()

    # Проверим
    assert len(servers) == 1
    assert servers[0]["name"] == "saved-server"
    assert servers[0]["ip"] == "2.2.2.2"

    # Удалим временный файл
    if os.path.exists("servers.json"):
        os.remove("servers.json")
