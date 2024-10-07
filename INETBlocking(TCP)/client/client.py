import socket  # Імпортуємо модуль для роботи з сокетами
import time  # Імпортуємо модуль для вимірювання часу

# Налаштування клієнта
SERVER_HOST = '127.0.0.1'  # Локальний хост (адреса сервера)
SERVER_PORT = 65432  # Порт сервера
BUFFER_SIZE = 4096  # Розмір буфера для отримання даних

# Тип пакету: 'small' або 'large'
packet_type = 'large'  # Вибираємо тип пакета (малий або великий)
packet_count = 10000  # Кількість пакетів для відправки

# Розміри пакетів для різних конфігурацій
SMALL_PACKET = b'M' * 64  # Створюємо малий пакет (64 байти даних)
LARGE_PACKET = b'L' * 1024  # Створюємо великий пакет (1024 байти даних)

# Вибір типу пакета
MESSAGE = SMALL_PACKET if packet_type == 'small' else LARGE_PACKET  # Вибір пакета для відправки

# Функція для вимірювання часу підключення
def measure_connection_time():
    start_time = time.time()  # Визначаємо час початку
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Створюємо TCP сокет
    client_socket.connect((SERVER_HOST, SERVER_PORT))  # Підключаємося до сервера
    connection_time = time.time() - start_time  # Визначаємо тривалість підключення
    return client_socket, connection_time  # Повертаємо сокет та час підключення

# Основна функція клієнта
def start_client():
    byte_count = 0  # Лічильник загальної кількості байт

    client_socket, connection_time = measure_connection_time()  # Отримуємо сокет і час підключення
    print(f'Клієнт TCP підключений до сервера за {connection_time:.4f} секунд')  # Виводимо повідомлення

    start_time = time.time()  # Визначаємо час початку передачі

    try:
        for i in range(packet_count):  # Цикл відправки пакетів
            client_socket.sendall(MESSAGE)  # Відправляємо пакет
            byte_count += len(MESSAGE)  # Підраховуємо кількість байт
            response = client_socket.recv(BUFFER_SIZE)  # Отримуємо підтвердження від сервера
            print(f'Отримано підтвердження для пакета №{i + 1}')  # Виводимо підтвердження
    except KeyboardInterrupt:  # Переривання роботи (наприклад, через Ctrl+C)
        pass
    finally:
        client_socket.close()  # Закриваємо сокет

    # Визначаємо тривалість передачі
    duration = time.time() - start_time
    packets_per_sec = packet_count / duration  # Кількість пакетів за секунду
    bytes_per_sec = byte_count / duration  # Кількість байтів за секунду
    avg_packet_size = byte_count / packet_count if packet_count else 0  # Середній розмір пакета

    # Виводимо результати
    print(f'Статистика:\nПакетів/сек: {packets_per_sec:.2f}\nБайтів/сек: {bytes_per_sec:.2f}')
    print(f'Загальна кількість відправлених пакетів: {packet_count}, Загальна кількість байт: {byte_count}')
    print(f'Середній розмір пакета: {avg_packet_size:.2f} байт')
    print(f'Тест тривав: {duration:.2f} секунд')

if __name__ == "__main__":  # Запускаємо клієнт, якщо цей файл виконується напряму
    start_client()  # Викликаємо основну функцію клієнта
