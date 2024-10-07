import socket  # Імпортуємо модуль для роботи з сокетами
import time  # Імпортуємо модуль для вимірювання часу

# Налаштування сервера
SERVER_HOST = '127.0.0.1'  # Адреса сервера (localhost)
SERVER_PORT = 65432  # Порт сервера
BUFFER_SIZE = 4096  # Розмір буфера для отримання даних

def measure_performance(start_time, packet_count, byte_count, expected_packet_count):
    duration = time.time() - start_time  # Обчислюємо тривалість
    packets_per_sec = packet_count / duration if duration > 0 else 0  # Обчислюємо кількість пакетів за секунду
    bytes_per_sec = byte_count / duration if duration > 0 else 0  # Обчислюємо кількість байтів за секунду
    lost_packets = expected_packet_count - packet_count  # Обчислюємо кількість втрачених пакетів
    average_packet_size = byte_count / packet_count if packet_count else 0  # Обчислюємо середній розмір пакета
    return packets_per_sec, bytes_per_sec, lost_packets, average_packet_size, duration  # Повертаємо статистику

def start_server(expected_packet_count):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Створюємо TCP сокет
    server_socket.bind((SERVER_HOST, SERVER_PORT))  # Прив'язуємо сокет до адреси та порту
    server_socket.listen(1)  # Слухаємо один вхідний зв'язок
    print(f'TCP сервер очікує на підключення на {SERVER_HOST}:{SERVER_PORT}')  # Повідомляємо про готовність

    conn, addr = server_socket.accept()  # Приймаємо підключення
    print(f'Підключено клієнта {addr}')  # Виводимо інформацію про підключення

    packet_count = 0  # Лічильник отриманих пакетів
    byte_count = 0  # Лічильник отриманих байт
    start_time = None  # Ініціалізуємо час початку як None

    try:
        while packet_count < expected_packet_count:  # Продовжуємо приймати дані до досягнення очікуваної кількості пакетів
            data = conn.recv(BUFFER_SIZE)  # Отримуємо пакет від клієнта
            if not data:  # Якщо даних немає, виходимо з циклу
                break
            
            if start_time is None:  # Якщо це перший пакет
                start_time = time.time()  # Фіксуємо час початку приймання даних
            
            packet_count += 1  # Збільшуємо лічильник отриманих пакетів
            byte_count += len(data)  # Підраховуємо кількість отриманих байт
            print(f'Отримано пакет №{packet_count}, розмір: {len(data)} байт')  # Виводимо інформацію про отриманий пакет
            conn.sendall(b'ACK')  # Відправляємо підтвердження клієнту
    except KeyboardInterrupt:  # Якщо роботу перервуть, зупиняємо сокет
        pass
    finally:
        conn.close()  # Закриваємо з'єднання
        server_socket.close()  # Закриваємо сокет після завершення роботи

    # Викликаємо функцію для обчислення продуктивності
    packets_per_sec, bytes_per_sec, lost_packets, avg_packet_size, total_duration = measure_performance(
        start_time, packet_count, byte_count, expected_packet_count
    )
    # Виводимо статистику
    print(f'Статистика:\nПакетів/сек: {packets_per_sec:.2f}\nБайтів/сек: {bytes_per_sec:.2f}')
    print(f'Втрачено пакетів: {lost_packets}, Загальна кількість: {packet_count}')
    print(f'Середній розмір пакета: {avg_packet_size:.2f} байт')
    print(f'Загальна тривалість: {total_duration:.2f} секунд')

if __name__ == "__main__":  # Основний блок запуску сервера
    expected_packet_count = 10000  # Очікувана кількість пакетів для оцінки втрат
    start_server(expected_packet_count)  # Викликаємо функцію запуску сервера
