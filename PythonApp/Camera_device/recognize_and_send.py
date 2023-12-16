import json
import cv2
import requests
import numpy as np
import mediapipe as mp
import tensorflow as tf
import os

api_url = 'http://192.168.2.239:8080/execute'

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in
                     results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
    face = np.array([[res.x, res.y, res.z] for res in
                     results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468 * 3)
    lh = np.array([[res.x, res.y, res.z] for res in
                   results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    rh = np.array([[res.x, res.y, res.z] for res in
                   results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(
        21 * 3)
    return np.concatenate([pose, lh, rh])



def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writeable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR COVERSION RGB 2 BGR
    return image, results


def draw_styled_landmarks(image, results, mp_holistic, mp_drawing):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                              mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                              mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
                              )
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                              )
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                              )
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                              )


def send_data_to_api(command_to_send):
    try:
        response = requests.post(api_url, json={'command': command_to_send})
        print(response.json())

    except Exception as e:
        print(f"Error: {e}")

def load_model():
    while True:
                try:
                    interpreter = tf.lite.Interpreter(model_path='my_model.tflite')
                    interpreter.allocate_tensors()
                    break
                except Exception as e:
                    print(e)
                    pass
    return interpreter

def read_action_labels():
    while True:
        try:
            with open('./action_names.json', 'r') as file:
                actions = json.load(file)
                return actions
        except:
            pass

def recognize(): 
    mp_holistic = mp.solutions.holistic  # Holistic model
    mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
    sequence = []
    threshold = 0.95

    actions = np.array(read_action_labels())

    cap = cv2.VideoCapture(0)
    # Set mediapipe model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            model = load_model()

            # Read feed
            ret, frame = cap.read()

            # Make detections
            image, results = mediapipe_detection(frame, holistic)

            draw_styled_landmarks(image, results, mp_holistic, mp_drawing)

            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-20:]

            if len(sequence) == 20:
                input_tensor_index = model.get_input_details()[0]['index']
                model.set_tensor(input_tensor_index, np.expand_dims(sequence, axis=0).astype(np.float32))

                model.invoke()

                output_tensor_index = model.get_output_details()[0]['index']
                res = model.get_tensor(output_tensor_index)[0]

                if res[np.argmax(res)] > threshold:
                    command = actions[np.argmax(res)]
                    print(command)
                    send_data_to_api(command)

        cap.release()


if __name__ == "__main__":
    recognize()
