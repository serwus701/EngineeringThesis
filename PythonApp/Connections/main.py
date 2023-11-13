import socket
import threading


def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Received: {request.decode('utf-8')}")

    # Send a simple response back to the client
    response = "Hello from the server!"
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Listening on 0.0.0.0:{port}")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


if __name__ == "__main__":
    port = 8080
    start_server(port)
