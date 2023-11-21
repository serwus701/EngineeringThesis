import json
import pickle
import socket

def receive_model():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Define the address and port to bind
        host = 'localhost'
        port = 12345

        try:
            # Bind the socket to the address and port
            s.bind((host, port))

            # Listen for incoming connections
            s.listen()

            print(f"Listening for connections on {host}:{port}")

            # Accept a connection
            conn, addr = s.accept()
            print(f"Accepted connection from {addr}")

            # Receive the model name
            name_bytes = conn.recv(4096)
            received_name = name_bytes.decode('utf-8')
            write_name_to_file(received_name)
            print(f"Received model name: {received_name}")

            # Receive the trained model
            model_bytes = b""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                model_bytes += data

            # Deserialize the received bytes to get the model
            received_model = pickle.loads(model_bytes)

            return received_model

        finally:
            # Close the connection and the socket
            conn.close()
            s.close()

def write_name_to_file(received_name):
    with open('action_names.json', 'r') as f:
        action_names = json.load(f)
        action_names.append(received_name)


if __name__ == "__main__":
    while True:
        try:
            received_model = receive_model()
            received_model.save('my_model.keras')
        except:
            pass