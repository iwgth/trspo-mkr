import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np

def calculate_element(row, col, matrix_a, matrix_b, result_matrix):
    result_matrix[row, col] = np.dot(matrix_a[row, :], matrix_b[:, col])

def handle_client(client_socket):
    try:
        matrix_sizes = client_socket.recv(1024).decode().split(',')
        n, m, l = map(int, matrix_sizes)

        print(f"Сервер прийняв матриці розміром: {n} x {m} and {m} x {l}")

        if n <= 0 or m <= 0 or l <= 0:
            raise ValueError("Значення матриці мають бути більше нуля")

        matrix_a_data = client_socket.recv(n * m * 4)  # Assuming int32 for simplicity
        matrix_b_data = client_socket.recv(m * l * 4)

        if len(matrix_a_data) != n * m * 4 or len(matrix_b_data) != m * l * 4:
            raise ValueError("Неправильний формат матриці")

        matrix_a = np.frombuffer(matrix_a_data, dtype=int).reshape(n, m)
        matrix_b = np.frombuffer(matrix_b_data, dtype=int).reshape(m, l)

        print("Сервер прийняв матриці")
        print("Матриця A:")
        print(matrix_a)
        print("Матриця B:")
        print(matrix_b)

        result_matrix = np.zeros((n, l), dtype=int)

        with ThreadPoolExecutor(max_workers=4) as executor:
            for i in range(n):
                for j in range(l):
                    executor.submit(calculate_element, i, j, matrix_a, matrix_b, result_matrix)

        print("Сервер надсилає результат до клієнта")
        client_socket.send(result_matrix.tobytes())
    except ValueError as ve:
        print(f"Сервер Error: {ve}")
    except Exception as e:
        print(f"Сервер Error: {e}")
    finally:
        client_socket.close()
        print("Сервер закрив конект")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Сервер прослуховує порт 12345")

    while True:
        client, addr = server.accept()
        print(f"Сервер прийняв конект {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    start_server()
