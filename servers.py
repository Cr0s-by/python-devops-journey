import os
import shutil
from datetime import datetime
import re
import json

# Пытаемся загрузить конфигурацию из файла config.json
try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    print("✅ Конфигурация загружена")

# Если файл config.json не найден (например, первый запуск)
except FileNotFoundError:
    print("⚠️ Файл config.json не найден. Используются значения по умолчанию")
    config = {
        "default_cpu": 8,
        "default_ram": 16,
        "data_file": "../servers.json",
        "app_name": "Учёт серверов"
    }

# Список для хранения всех серверов (изначально пустой)
servers = []


# Функция проверки, является ли строка корректным IP-адресом
def is_valid_ip(ip):
    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(pattern, ip)
    if not match:
        return False
    return all(0 <= int(part) <= 255 for part in match.groups())


# Функция добавления нового сервера
def add_server():
    name = input("Имя: ")
    ip = input("IP: ")
    role = input("Роль (web, db, cache): ")
    status = input("Статус (online/offline): ")
    standart = input("Оставить по умолчанию? (y/n): ")

    if standart == "y":
        cpu = config["default_cpu"]
        ram = config["default_ram"]
    else:
        cpu = int(input("CPU: "))
        ram = int(input("RAM (ГБ): "))

    # Создаём словарь с информацией о сервере
    server = {
        "name": name,
        "ip": ip,
        "role": role,
        "status": status,
        "cpu": cpu,
        "ram": ram
    }

    # Добавляем сервер в общий список
    servers.append(server)
    print(f"✅ Сервер {name} добавлен!")


# Функция вывода всех серверов
def list_servers():
    if not servers:
        print("Серверов пока нет.")
        return

    print("\nСписок серверов:")
    for server in servers:
        print(
            f"  {server['name']} | {server['ip']} | {server['role']} | {server['status']} | {server['cpu']} ядер, {server['ram']} ГБ")
    print()


# Функция поиска сервера по IP
def find_server_by_ip(ip):
    for server in servers:
        if is_valid_ip(ip):
            if server["ip"] == ip:
                print(f"Найден сервер: {server['name']} | {server['role']} | {server['status']}")
                return
        else:
            print("❌ Неверный формат IP-адреса")
            return
    print("❌ Сервер с таким IP не найден.")


# Функция удаления сервера по имени
def remove_server(name):
    for server in servers:
        if server["name"] == name:
            servers.remove(server)
            print(f"✅ Сервер {name} удалён.")
            return
    print("❌ Сервер не найден.")


# Функция вывода серверов в статусе "online"
def online_servers():
    found = False
    print("\nСерверы в статусе 'online':")
    for server in servers:
        if server["status"] == "online":
            print(f"  {server['name']} | {server['ip']} | {server['role']} | {server['cpu']} ядер, {server['ram']} ГБ")
            found = True
    if not found:
        print("  ❌ Нет серверов в статусе 'online'")
    print()


# Функция подсчёта общего количества серверов и суммарной RAM
def calculate_servers_and_ram():
    count = 0
    total_ram = 0
    for server in servers:
        count += 1
        total_ram += int(server["ram"])
    print(f"Количество серверов: {count}")
    print(f"Кол-во RAM: {total_ram}")


# Функция загрузки серверов из файла
def load_servers():
    global servers
    path = config["data_file"]
    print(f"Попытка загрузить из: {os.path.abspath(path)}")
    try:
        with open(path, "r", encoding="utf-8") as file:
            servers = json.load(file)
            print("✅ Данные загружены из", path)
            print("Содержимое:", servers)
    except FileNotFoundError:
        print("⚠️ Файл", path, "не найден. Начинаем с пустого списка.")
        servers = []
    except json.JSONDecodeError:
        print("❌ Ошибка чтения JSON. Начинаем с пустого списка.")
        servers = []


# Функция сохранения серверов в файл
def save_servers():
    print(f"💾 Сохраняю в: {os.path.abspath(config['data_file'])}")
    with open(config["data_file"], "w", encoding="utf-8") as file:
        json.dump(servers, file, ensure_ascii=False, indent=4)
    print("✅ Данные сохранены в servers.json")


def create_backup():
    # Папка для бэкапов
    backup_dir = "backups"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✅ Создана папка {backup_dir}")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"backup_{timestamp}.json"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        shutil.copy("servers.json", backup_path)
        print(f"✅ Бэкап создан: {backup_path}")
    except FileNotFoundError:
        print("❌ Не удалось создать бэкап: файл servers.json не найден")
    except Exception as e:
        print(f"❌ Ошибка при создании бэкапа: {e}")


if __name__ == "__main__":
    # ЗАГРУЖАЕМ ДАННЫЕ ПРИ СТАРТЕ ПРОГРАММЫ
    load_servers()

    # ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ — МЕНЮ
    while True:
        # Выводим название программы из конфига
        print(f"\n=== {config['app_name']} ===")
        print("1. Добавить сервер")
        print("2. Просмотреть все серверы")
        print("3. Найти сервер по IP")
        print("4. Удалить сервер по имени")
        print("5. Найти серверы online")
        print("6. Найти кол-во серверов и сумму RAM")
        print("7. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            add_server()
        elif choice == "2":
            list_servers()
        elif choice == "3":
            ip = input("Введите IP: ")
            find_server_by_ip(ip)
        elif choice == "4":
            name = input("Введите имя сервера: ")
            remove_server(name)
        elif choice == "5":
            online_servers()
        elif choice == "6":
            calculate_servers_and_ram()
        elif choice == "7":
            save_servers()
            create_backup()
            print("👋 Выход из программы.")
            break
        else:
            print("❗ Неверный выбор. Попробуйте снова.")
