import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np
#dev1
def handle_client(client_socket):
    try:
        matrix_sizes = client_socket.recv(1024).decode().split(',')
        n, m, l = map(int, matrix_sizes)

        print(f"From server: Received matrix sizes: {n} x {m} and {m} x {l}")

        if n <= 0 or m <= 0 or l <= 0:
            raise ValueError("Matrix dimensions must be positive integers")

        matrix_a_data = client_socket.recv(n * m * 4)  # Assuming int32 for simplicity
        matrix_b_data = client_socket.recv(m * l * 4)

        if len(matrix_a_data) != n * m * 4 or len(matrix_b_data) != m * l * 4:
            raise ValueError("Invalid matrix data received")

        matrix_a = np.frombuffer(matrix_a_data, dtype=int).reshape(n, m)
        matrix_b = np.frombuffer(matrix_b_data, dtype=int).reshape(m, l)

        print("From server: Received matrices:")
        print("Matrix A:")
        print(matrix_a)
        print("Matrix B:")
        print(matrix_b)

        # Perform matrix multiplication in a separate thread
        with ThreadPoolExecutor(max_workers=1) as executor:
            result_matrix = executor.submit(np.dot, matrix_a, matrix_b).result()

        print("Sending result matrix to client")
        client_socket.send(result_matrix.tobytes())
    except ValueError as ve:
        print(f"From server: Error: {ve}")
    except Exception as e:
        print(f"From server: Error: {e}")
    finally:
        client_socket.close()
        print("From server: Connection closed")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Server listening on port 12345")

    while True:
        client, addr = server.accept()
        print(f"From server: accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    start_server()
