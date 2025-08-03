import socket
import threading

# Глобальный список всех подключённых клиентов
clients = []


def broadcast(message):

    for client in clients.copy():  # Используем копию для безопасного удаления
        try:
            client.send(message.encode())
        except (ConnectionError, OSError):
            # Если отправка не удалась, удаляем клиента из списка
            clients.remove(client)


def handle_client(conn, addr):

    print(f"[Новое подключение] {addr}")
    clients.append(conn)

    try:
        while True:
            # Получаем сообщение от клиента
            data = conn.recv(1024)
            if not data:
                break  # Клиент отключился

            decoded_message = data.decode()
            print(f"[{addr}] Отправлено: {decoded_message}")

            # Формируем сообщение для рассылки
            formatted_message = f"[{addr[0]}:{addr[1]}] {decoded_message}"

            # Рассылаем всем клиентам
            broadcast(formatted_message)

    except ConnectionResetError:
        print(f"[Отключение] {addr} разорвал соединение")
    finally:
        # Удаляем клиента из списка и закрываем соединение
        if conn in clients:
            clients.remove(conn)
        conn.close()
        print(f"[Активные подключения] {len(clients)}")


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server.bind(("127.0.0.1", 50000))
    server.bind(("DESKTOP-FLB21SC", 50000))  # Слушаем все интерфейсы
    server.listen()
    print(f"[Сервер запущен] Ожидание подключений на порту 50000...")

    try:
        while True:
            # Принимаем новое подключение
            conn, addr = server.accept()

            # Запускаем поток для обработки клиента
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

            # Выводим статистику
            print(f"[Активные подключения] {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\n[Остановка сервера]")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
