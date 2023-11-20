from flask import Flask, request, jsonify
from tensorflow import keras

app = Flask(__name__)

@app.route('/receive_model', methods=['POST'])
def receive_model():
    try:
        # Receive the model JSON and weights from the sender
        model_json = request.files['model_json'].read().decode('utf-8')
        model_weights = request.files['model_weights']

        # Convert the JSON to a Keras model
        received_model = keras.models.model_from_json(model_json)

        # Load the weights into the model
        received_model.load_weights(model_weights)

        # Save the received model
        received_model.save('received_model.keras')

        return jsonify({'message': 'Model received and saved successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000)