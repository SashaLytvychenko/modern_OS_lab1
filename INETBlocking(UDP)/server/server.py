import socket  # Імпортуємо модуль для роботи з сокетами
import time  # Імпортуємо модуль для вимірювання часу

# Налаштування сервера
SERVER_HOST = '127.0.0.1'  # Адреса сервера (localhost)
SERVER_PORT = 65431  # Порт сервера
BUFFER_SIZE = 4096 * 200  # Розмір буфера для отримання даних (збільшений для UDP)

# Функція для вимірювання швидкодії
def measure_performance(start_time, packet_count, byte_count):
    duration = time.time() - start_time  # Обчислюємо тривалість приймання даних
    packets_per_sec = packet_count / duration if duration > 0 else 0  # Обчислюємо кількість пакетів за секунду
    bytes_per_sec = byte_count / duration if duration > 0 else 0  # Обчислюємо кількість байтів за секунду
    lost_packets = 0  # Для UDP втрати пакетів не вимірюємо, тому тут завжди 0
    average_packet_size = byte_count / packet_count if packet_count else 0  # Обчислюємо середній розмір пакета
    return packets_per_sec, bytes_per_sec, lost_packets, average_packet_size, duration  # Повертаємо статистику

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Створюємо UDP сокет
    server_socket.bind((SERVER_HOST, SERVER_PORT))  # Прив'язуємо сокет до адреси та порту
    print(f'UDP сервер очікує на пакети на {SERVER_HOST}:{SERVER_PORT}')  # Виводимо повідомлення про очікування

    packet_count = 0  # Лічильник отриманих пакетів
    byte_count = 0  # Лічильник отриманих байт
    start_time = None  # Ініціалізуємо час початку як None
    first_packet_received = False  # Позначаємо, чи отримано перший пакет

    try:
        while True:  # Продовжуємо приймати дані без обмежень
            if first_packet_received:
                server_socket.settimeout(0.1)  # Встановлюємо таймаут у 0.1 секунди для recvfrom
            else:
                server_socket.settimeout(None)  # Без таймауту до отримання першого пакета

            try:
                data, addr = server_socket.recvfrom(BUFFER_SIZE)  # Отримуємо пакет від клієнта
                if not data:  # Якщо даних немає, виходимо з циклу
                    break
                if not first_packet_received:  # Якщо це перший пакет
                    start_time = time.time()  # Фіксуємо час початку приймання даних
                    first_packet_received = True  # Отримали перший пакет
                packet_count += 1  # Збільшуємо лічильник отриманих пакетів
                byte_count += len(data)  # Підраховуємо кількість отриманих байт
                print(f'Отримано пакет №{packet_count} від {addr}, розмір: {len(data)} байт')  # Виводимо інформацію про отриманий пакет
            except socket.timeout:
                print('Таймаут. Завершення приймання пакетів.')  # Виводимо повідомлення про таймаут
                break  # Виходимо з циклу при таймауті
    except KeyboardInterrupt:  # Якщо роботу перервуть, зупиняємо сокет
        pass
    finally:
        server_socket.close()  # Закриваємо сокет після завершення роботи

    # Викликаємо функцію для обчислення продуктивності, якщо був отриманий хоча б один пакет
    if packet_count > 0:
        packets_per_sec, bytes_per_sec, lost_packets, avg_packet_size, total_duration = measure_performance(
            start_time, packet_count, byte_count
        )
        # Виводимо статистику
        print(f'Статистика:\nПакетів/сек: {packets_per_sec:.2f}\nБайтів/сек: {bytes_per_sec:.2f}')
        print(f'Втрачено пакетів: {lost_packets}, Загальна кількість: {packet_count}')
        print(f'Середній розмір пакета: {avg_packet_size:.2f} байт')
        print(f'Загальна тривалість: {total_duration:.2f} секунд')
    else:
        print('Не було отримано жодного пакета.')

if __name__ == "__main__":  # Основний блок запуску сервера
    start_server()  # Викликаємо функцію запуску сервера
