import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_action():
    try:
        # Receive the action name from the client
        action_name = request.json.get('command')
        if check_if_active():
            print(action_name)
        else:
            print("App is not active")

        os.startfile(os.getcwd() + "/actions_exe/" + get_mapped_action_name(action_name) + ".exe")

        return jsonify({'message': 'Action executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

def start_server(port):
    app.run(host='0.0.0.0', port=port, threaded=True)

def check_if_active():
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
    
def get_mapped_action_name(recieved_action_name):
    try:
        with open('../UI/status.json') as f:
            data = json.load(f)
            if not data.get("dropdowns", {}).get(recieved_action_name, {}).get("active", False):
                return "none"
            mapped_name = data.get("dropdowns", {}).get(recieved_action_name, {}).get("value", "none")
            return mapped_name
    except Exception as e:
        print(e)
        return "none"
    
        
if __name__ == "__main__":
    port = 8080
    start_server(port)