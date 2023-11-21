import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_action():
    try:
        # Receive the action name from the client
        action_name = request.json.get('command')
        if check_if_app_is_active():
            print(action_name)
        else:
            print("App is not active")

        # Perform the desired action (for example, executing an executable file)
        # os.startfile(os.getcwd() + "/actions_exe/" + action_name + ".exe")

        return jsonify({'message': 'Action executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

def start_server(port):
    app.run(host='0.0.0.0', port=port, threaded=True)

def check_if_app_is_active():
    try:
        with open('../UI/status.json') as f:
            data = json.load(f)
            if data['app_status'] == False:
                print("content false")
                return False
        print("content true")
        return True
    except:
        print("no file")
        return False

if __name__ == "__main__":
    port = 8080
    start_server(port)