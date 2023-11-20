from flask import Flask, request, jsonify
import os
import threading

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_action():
    try:
        # Receive the action name from the client
        action_name = request.json.get('command')
        print(action_name)

        # Perform the desired action (for example, executing an executable file)
        os.startfile(os.getcwd() + "/actions_exe/" + action_name + ".exe")

        return jsonify({'message': 'Action executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

def start_server(port):
    app.run(host='0.0.0.0', port=port, threaded=True)

if __name__ == "__main__":
    port = 8080
    start_server(port)