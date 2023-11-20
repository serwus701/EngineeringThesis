import pickle
import socket
from flask import Flask, request, jsonify
from tensorflow import keras
import numpy as np
import json

def receive_model():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

received_model = receive_model()
received_model.save('dupa.keras')