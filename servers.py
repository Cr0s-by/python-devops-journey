import os
import shutil
from datetime import datetime
import re
import json

# Пытаемся загрузить конфигурацию из файла config.json
try:
    # Открываем файл config.json для чтения (режим "r")
    with open("config.json", "r", encoding="utf-8") as file:
        # Загружаем данные из файла в переменную config (это будет словарь)
        config = json.load(file)
    # Сообщаем, что конфиг загружен
    print("✅ Конфигурация загружена")

# Если файл config.json не найден (например, первый запуск)
except FileNotFoundError:
    # Выводим предупреждение
    print("⚠️ Файл config.json не найден. Используются значения по умолчанию")
    # Создаём словарь config вручную — это "запасной" вариант
    config = {
        "default_cpu": 8,  # CPU по умолчанию
        "default_ram": 16,  # RAM по умолчанию
        "data_file": "../servers.json",  # Имя файла для хранения серверов
        "app_name": "Учёт серверов"  # Название программы
    }

# Список для хранения всех серверов (изначально пустой)
servers = []


# Функция проверки, является ли строка корректным IP-адресом
def is_valid_ip(ip):
    # Шаблон: 4 числа от 0 до 999, разделённые точками
    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    # Проверяем, подходит ли строка под шаблон
    match = re.match(pattern, ip)
    # Если не подходит — возвращаем False
    if not match:
        return False
    # Проверяем, что каждое число от 0 до 255
    return all(0 <= int(part) <= 255 for part in match.groups())


# Функция добавления нового сервера
def add_server():
    # Спрашиваем у пользователя данные
    name = input("Имя: ")
    ip = input("IP: ")
    role = input("Роль (web, db, cache): ")
    status = input("Статус (online/offline): ")
    standart = input("Оставить по умолчанию? (y/n): ")

    # Если пользователь выбрал "по умолчанию"
    if standart == "y":
        # Берём значения из конфига
        cpu = config["default_cpu"]
        ram = config["default_ram"]
    else:
        # Иначе спрашиваем вручную
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
    # Сообщаем, что сервер добавлен
    print(f"✅ Сервер {name} добавлен!")


# Функция вывода всех серверов
def list_servers():
    # Если список пуст — сообщаем и выходим
    if not servers:
        print("Серверов пока нет.")
        return

    print("\nСписок серверов:")
    # Перебираем все серверы и выводим их
    for server in servers:
        print(
            f"  {server['name']} | {server['ip']} | {server['role']} | {server['status']} | {server['cpu']} ядер, {server['ram']} ГБ")
    print()


# Функция поиска сервера по IP
def find_server_by_ip(ip):
    # Перебираем все серверы
    for server in servers:
        # Сначала проверяем, корректный ли IP
        if is_valid_ip(ip):
            # Если IP совпадает — выводим сервер и выходим
            if server["ip"] == ip:
                print(f"Найден сервер: {server['name']} | {server['role']} | {server['status']}")
                return
        else:
            # Если IP некорректный — сообщаем и выходим
            print("❌ Неверный формат IP-адреса")
            return
    # Если цикл закончился, а сервер не найден
    print("❌ Сервер с таким IP не найден.")


# Функция удаления сервера по имени
def remove_server(name):
    # Перебираем серверы
    for server in servers:
        # Если нашли по имени
        if server["name"] == name:
            # Удаляем из списка
            servers.remove(server)
            print(f"✅ Сервер {name} удалён.")
            return
    # Если не нашли
    print("❌ Сервер не найден.")


# Функция вывода серверов в статусе "online"
def online_servers():
    # Флаг: найден ли хотя бы один online-сервер
    found = False
    print("\nСерверы в статусе 'online':")
    # Перебираем все серверы
    for server in servers:
        if server["status"] == "online":
            print(f"  {server['name']} | {server['ip']} | {server['role']} | {server['cpu']} ядер, {server['ram']} ГБ")
            found = True  # Отмечаем, что нашли
    # Если ни одного не нашли
    if not found:
        print("  ❌ Нет серверов в статусе 'online'")
    print()


# Функция подсчёта общего количества серверов и суммарной RAM
def calculate_servers_and_ram():
    count = 0  # Счётчик серверов
    total_ram = 0  # Сумма RAM
    # Перебираем все серверы
    for server in servers:
        count += 1
        total_ram += int(server["ram"])
    # Выводим результат
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
            print("Содержимое:", servers)  # Добавляем эту строку
    except FileNotFoundError:
        print("⚠️ Файл", path, "не найден. Начинаем с пустого списка.")
        servers = []
    except json.JSONDecodeError:
        print("❌ Ошибка чтения JSON. Начинаем с пустого списка.")
        servers = []


# Функция сохранения серверов в файл
def save_servers():
    # Открываем файл для записи (режим "w")
    print(f"💾 Сохраняю в: {os.path.abspath(config['data_file'])}")
    with open(config["data_file"], "w", encoding="utf-8") as file:
        json.dump(servers, file, ensure_ascii=False, indent=4)
    print("✅ Данные сохранены в servers.json")


def create_backup():
    # Папка для бэкапов
    backup_dir = "backups"

    # Создаём папку, если её нет
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✅ Создана папка {backup_dir}")

    # Генерируем имя файла с датой и временем
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"backup_{timestamp}.json"
    backup_path = os.path.join(backup_dir, backup_filename)

    # Копируем файл
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

        # Спрашиваем, что хочет пользователь
        choice = input("\nВыберите действие: ")

        # Обрабатываем выбор
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
            create_backup()  # Добавь эту строку
            print("👋 Выход из программы.")
            break
        else:
            print("❗ Неверный выбор. Попробуйте снова.")
