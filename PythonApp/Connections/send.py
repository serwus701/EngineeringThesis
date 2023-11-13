import socket
import time
import random


def send_data(server_address, server_port):
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client.connect((server_address, server_port))

    message = "1"

    print(f"Sending message: {message}")
    client.send(message.encode('utf-8'))

    # Receive the response from the server
    response = client.recv(1024)
    print(f"Received from server: {response.decode('utf-8')}")

    # Close the socket connection
    client.close()


if __name__ == "__main__":
    server_address = '192.168.2.239'  # Replace with the actual server address
    server_port = 8080  # Replace with the actual server port

    send_data(server_address, server_port)
