import json
import pickle
import socket

import tensorflow

def receive_model():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Define the address and port to bind
        host = 'localhost'
        port = 12345

        try:
            s.bind((host, port))
            s.listen()

            print(f"Listening for connections on {host}:{port}")
            conn, addr = s.accept()
            print(f"Accepted connection from {addr}")
            
            name_bytes = conn.recv(4096)
            received_name = name_bytes.decode('utf-8')
            write_name_to_file(received_name)
            print(f"Received model name: {received_name}")
            model_bytes = b""

            while True:
                data = conn.recv(4096)
                if not data:
                    break
                model_bytes += data
            received_model = pickle.loads(model_bytes)

            return received_model

        finally:
            conn.close()
            s.close()

def write_name_to_file(received_name):
    with open('action_names.json', 'r') as f:
        action_names = json.load(f)
        action_names.append(received_name)

def save_model_as_tflite(base_model):
    output_model = "./my_model.tflite"

    converter = tensorflow.lite.TFLiteConverter.from_keras_model(base_model)
    converter.target_spec.supported_ops = [tensorflow.lite.OpsSet.TFLITE_BUILTINS, tensorflow.lite.OpsSet.SELECT_TF_OPS]
    converter._experimental_lower_tensor_list_ops = False

    tflite_quant_model = converter.convert()
    with open(output_model, 'wb') as o:
        o.write(tflite_quant_model)

if __name__ == "__main__":
    while True:
        try:
            received_model = receive_model()
            received_model.save('my_model.keras')
            save_model_as_tflite(received_model)
        except:
            pass