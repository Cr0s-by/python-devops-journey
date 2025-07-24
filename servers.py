import re

servers = []


def is_valid_ip(ip):
    pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(pattern, ip)
    if not match:
        return False
    # Проверяем, что каждое число <= 255
    return all(0 <= int(part) <= 255 for part in match.groups())


def add_server():
    name = input("Имя: ")
    ip = input("IP: ")
    role = input("Роль (web, db, cache): ")
    status = input("Статус (online/offline): ")
    print(f"Оставить по умолчанию? (y/n):")
    standart = input()
    if standart == "y":
        cpu = 8
        ram = 16
    else:
        cpu = int(input("CPU: "))
        ram = int(input("RAM (ГБ): "))

    server = {
        "name": name,
        "ip": ip,
        "role": role,
        "status": status,
        "cpu": cpu,
        "ram": ram
    }

    servers.append(server)
    print(f"✅ Сервер {name} добавлен!")


def list_servers():
    if not servers:
        print("Серверов пока нет.")
        return

    print("\nСписок серверов:")
    for server in servers:
        print(
            f"  {server['name']} | {server['ip']} | {server['role']} | {server['status']} | {server['cpu']} ядер, {server['ram']} ГБ")
    print()


def find_server_by_ip(ip):
    for server in servers:
        if is_valid_ip(ip):
            if server["ip"] == ip:
                print(f"Найден сервер: {server['name']} | {server['role']} | {server['status']}")
                return
        else:
            print("❌ Неверный формат IP-адреса")
    print("❌ Сервер с таким IP не найден.")


def remove_server(name):
    for server in servers:
        if server["name"] == name:
            servers.remove(server)
            print(f"✅ Сервер {name} удалён.")
            return
    print("❌ Сервер не найден.")


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


def calculate_servers_and_ram():
    count = 0
    total_ram = 0
    for server in servers:
        count += 1
        total_ram += int(server["ram"])
    print(f"Количество серверов: {count}")
    print(f"Кол-во RAM: {total_ram}")


while True:
    print("\n=== Учёт серверов ===")
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
        print("👋 Выход из программы.")
        break
    else:
        print("❗ Неверный выбор. Попробуйте снова.")
