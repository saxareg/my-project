import socket
import threading

# Глобальный список всех подключённых клиентов
clients = []


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
