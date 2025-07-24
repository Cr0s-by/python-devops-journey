servers = []


def add_server():
    name = input("Имя: ")
    ip = input("IP: ")
    role = input("Роль (web, db, cache): ")
    status = input("Статус (online/offline): ")
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
        if server["ip"] == ip:
            print(f"Найден сервер: {server['name']} | {server['role']} | {server['status']}")
            return
    print("❌ Сервер с таким IP не найден.")


def remove_server(name):
    for server in servers:
        if server["name"] == name:
            servers.remove(server)
            print(f"✅ Сервер {name} удалён.")
            return
    print("❌ Сервер не найден.")


while True:
    print("\n=== Учёт серверов ===")
    print("1. Добавить сервер")
    print("2. Просмотреть все серверы")
    print("3. Найти сервер по IP")
    print("4. Удалить сервер по имени")
    print("5. Выход")

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
        print("👋 Выход из программы.")
        break
    else:
        print("❗ Неверный выбор. Попробуйте снова.")
