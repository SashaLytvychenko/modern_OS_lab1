import socket  # Імпортуємо модуль для роботи з сокетами
import time  # Імпортуємо модуль для вимірювання часу

# Налаштування клієнта
SERVER_HOST = '127.0.0.1'  # Адреса сервера (localhost)
SERVER_PORT = 65431  # Порт сервера
BUFFER_SIZE = 4096  # Розмір буфера для отримання даних

# Тип пакету: 'small' або 'large'
packet_type = 'large'  # Вибираємо тип пакета: малий або великий
packet_count = 10000  # Задаємо кількість пакетів для відправки

# Розміри пакетів для різних конфігурацій
SMALL_PACKET = b'M' * 64  # Створюємо малий пакет (64 байти даних)
LARGE_PACKET = b'L' * 1024  # Створюємо великий пакет (1024 байти даних)

# Вибір типу пакета
MESSAGE = SMALL_PACKET if packet_type == 'small' else LARGE_PACKET  # Вибираємо пакет для відправки в залежності від типу

# Функція для вимірювання часу підключення
def measure_connection_time():
    start_time = time.time()  # Запускаємо таймер
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Створюємо UDP сокет
    connection_time = time.time() - start_time  # Визначаємо час на створення сокета (для узгодженості з TCP)
    return client_socket, connection_time  # Повертаємо сокет та час підключення

def start_client():
    byte_count = 0  # Лічильник загальної кількості відправлених байт

    client_socket, connection_time = measure_connection_time()  # Отримуємо сокет і час підключення
    print(f'Клієнт UDP готовий відправляти пакети (псевдо-з’єднання за {connection_time:.4f} секунд)')  # Виводимо повідомлення

    start_time = time.time()  # Фіксуємо початок передачі даних

    try:
        for i in range(packet_count):  # Цикл відправки пакетів
            client_socket.sendto(MESSAGE, (SERVER_HOST, SERVER_PORT))  # Відправляємо пакет на сервер
            byte_count += len(MESSAGE)  # Підраховуємо кількість відправлених байт
            # Відсутнє підтвердження, оскільки UDP не гарантує його
    except KeyboardInterrupt:  # Якщо роботу перервуть, неочікувано закриваємо сокет
        pass
    finally:
        client_socket.close()  # Закриваємо сокет після завершення передачі

    duration = time.time() - start_time  # Визначаємо тривалість передачі
    packets_per_sec = packet_count / duration  # Обчислюємо кількість пакетів за секунду
    bytes_per_sec = byte_count / duration  # Обчислюємо кількість байтів за секунду
    avg_packet_size = byte_count / packet_count if packet_count else 0  # Середній розмір пакета

    # Виводимо статистику передачі
    print(f'Статистика:\nПакетів/сек: {packets_per_sec:.2f}\nБайтів/сек: {bytes_per_sec:.2f}')
    print(f'Загальна кількість відправлених пакетів: {packet_count}, Загальна кількість байт: {byte_count}')
    print(f'Середній розмір пакета: {avg_packet_size:.2f} байт')
    print(f'Тест тривав: {duration:.2f} секунд')

if __name__ == "__main__":  # Основний блок запуску клієнта
    start_client()  # Викликаємо функцію запуску клієнта
