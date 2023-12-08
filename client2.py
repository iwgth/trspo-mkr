import socket
import numpy as np
import time
#dev
def communicate_with_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))
    n, m, l = np.random.randint(1000, 2000, size=3)
    matrix_a = np.random.randint(1, 10, size=(n, m))
    matrix_b = np.random.randint(1, 10, size=(m, l))

    print(f"Generated matrix by client2:")
    print("Matrix A:")
    print(matrix_a)
    print("Matrix B:")
    print(matrix_b)

    print("Sending matrix sizes to server")
    client.send(f"{n},{m},{l}".encode())

    print("Sending matrices to server")
    client.send(matrix_a.tobytes())
    client.send(matrix_b.tobytes())

    result_data = b""
    while True:
        chunk = client.recv(4096)
        if not chunk:
            time.sleep(0.1)
            break
        result_data += chunk

    if len(result_data) == 0:
        print("Server closed")
    else:
        result_matrix = np.frombuffer(result_data, dtype=int).reshape(n, l)

        print("Received result matrix:")
        print(result_matrix)

    client.close()
    print("Connection closed")

if __name__ == "__main__":
    communicate_with_server()
