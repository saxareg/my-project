import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog  # Для запроса имени


class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Ychat")

        # Настройки соединения
        self.client_socket = socket.socket()
        self.port = 50000
        # self.host = "127.0.0.1"
        self.host = "DESKTOP-FLB21SC"

        # Интерфейс
        self.create_widgets()
        self.setup_connection()

        # Поток для получения сообщений
        self.receive_thread = threading.Thread(
            target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def create_widgets(self):

        # Область чата
        self.chat_area = ScrolledText(
            self.master, state='disabled', height=20, width=50)
        self.chat_area.pack(padx=10, pady=10)

        # Фрейм для ввода сообщений
        input_frame = Frame(self.master)
        input_frame.pack(padx=10, pady=(0, 10), fill=X)

        # Поле ввода сообщения
        self.message_entry = Entry(input_frame)
        self.message_entry.pack(side=LEFT, expand=True, fill=X)
        self.message_entry.bind("<Return>", self.send_message)

        # Кнопка отправки
        send_button = Button(input_frame, text="Отправить",
                             command=self.send_message)
        send_button.pack(side=RIGHT, padx=(5, 0))

    def setup_connection(self):

        # Запрос имени пользователя
        self.name = simpledialog.askstring(
            "Имя пользователя", "Введите ваше имя:", parent=self.master)
        if not self.name:
            self.name = "Аноним"

        try:
            self.client_socket.connect((self.host, self.port))
            self.display_message(
                "Система", f"Подключено к серверу как {self.name}")
        except Exception as e:
            self.display_message("Система", f"Ошибка подключения: {str(e)}")

    def send_message(self, event=None):

        message = self.message_entry.get()
        if message:
            try:
                full_message = f"{self.name}: {message}"
                self.client_socket.send(full_message.encode())
                self.message_entry.delete(0, END)
            except Exception as e:
                self.display_message("Система", f"Ошибка отправки: {str(e)}")

    def receive_messages(self):

        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                decoded_data = data.decode()
                if ":" in decoded_data:
                    name, message = decoded_data.split(":", 1)
                    self.display_message(name, message)
                else:
                    self.display_message("Сервер", decoded_data)
            except Exception as e:
                self.display_message("Система", f"Ошибка соединения: {str(e)}")
                break

    def display_message(self, sender, message):

        self.chat_area.configure(state='normal')
        self.chat_area.insert(END, f"{sender}: {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(END)

    def on_closing(self):

        try:
            self.client_socket.close()
        except:
            pass
        self.master.destroy()


if __name__ == "__main__":
    root = Tk()

    app = ChatClientGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
