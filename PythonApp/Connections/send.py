import socket
import time
import random


def send_data(server_address, server_port):
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client.connect((server_address, server_port))

    # Mocked condition to determine the message to send
    condition = random.choice([1, 2, 3])

    # Send different messages based on the mocked condition
    if condition == 1:
        message = "1"
    elif condition == 2:
        message = "2"
    else:
        message = "3"

    print(f"Sending message: {message}")
    client.send(message.encode('utf-8'))

    # Receive the response from the server
    response = client.recv(1024)
    print(f"Received from server: {response.decode('utf-8')}")

    # Close the socket connection
    client.close()


if __name__ == "__main__":
    server_address = '127.0.0.1'  # Replace with the actual server address
    server_port = 8080  # Replace with the actual server port

    while True:
        send_data(server_address, server_port)
        time.sleep(1)  # Sleep for 1 second before sending the next message
