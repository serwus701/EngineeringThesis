import cv2
import numpy as np
import os
import json
import requests
import mediapipe as mp
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities
DATA_PATH = os.path.join('MP_Data')
json_file_path = './actions_sequences.json'
server_address = '192.168.2.239'  # Replace with the actual server address
server_port = 8080
api_url = 'http://localhost:5000/receive_model'


def update_json(action_name, num_sequences):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data[action_name] = num_sequences

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)


def get_actions():
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    return np.array(list(data.keys()))


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writeable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR COVERSION RGB 2 BGR
    return image, results


def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)  # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)  # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks,
                              mp_holistic.HAND_CONNECTIONS)  # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks,
                              mp_holistic.HAND_CONNECTIONS)  # Draw right hand connections


def draw_styled_landmarks(image, results):
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


def manage_folders(action_name, no_sequences, data_path):
    for sequence in range(no_sequences):
        try:
            os.makedirs(os.path.join(data_path, action_name, str(sequence)))
        except:
            pass


def collect_data(action_name, no_sequences):
    sequence_length = 30
    cap = cv2.VideoCapture(0)
    manage_folders(action_name, no_sequences, DATA_PATH)
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        # Loop through sequences aka videos
        for sequence in range(no_sequences):
            # Loop through video length aka sequence length
            for frame_num in range(sequence_length):

                # Read feed
                ret, frame = cap.read()

                # Make detections
                image, results = mediapipe_detection(frame, holistic)
                #                 print(results)

                # Draw landmarks
                draw_styled_landmarks(image, results)

                # NEW Apply wait logic
                if frame_num == 0:
                    cv2.putText(image, 'STARTING COLLECTION', (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(action_name, sequence + 1),
                                (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    # Show to screen
                    cv2.imshow('OpenCV Feed', image)
                    cv2.waitKey(700)
                else:
                    cv2.putText(image,
                                'Collecting frames for {} {}/{}'.format(action_name, sequence + 1, sequence_length),
                                (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    # Show to screen
                    cv2.imshow('OpenCV Feed', image)

                # NEW Export keypoints
                keypoints = extract_keypoints(results)
                npy_path = os.path.join(DATA_PATH, action_name, str(sequence), str(frame_num))
                np.save(npy_path, keypoints)

                # Break gracefully
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
        cap.release()
        cv2.destroyAllWindows()


def build_and_train_NN(action, no_sequences):
    update_json(action, no_sequences)
    actions = get_actions()
    label_map = {label: num for num, label in enumerate(actions)}
    sequences, labels = np.load('./sequences.npy').tolist(), np.load('./labels.npy').tolist()

    for sequence in range(no_sequences):
        window = []
        for frame_num in range(30):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

    np.save('sequences.npy', np.array(sequences))
    np.save('labels.npy', np.array(labels))

    y = to_categorical(labels).astype(int)
    X = np.array(sequences)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

    log_dir = os.path.join('Logs')
    tb_callback = TensorBoard(log_dir=log_dir)

    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 258), name='lstm_1'))
    model.add(LSTM(128, return_sequences=True, activation='relu', name='lstm_2'))
    model.add(LSTM(64, return_sequences=False, activation='relu', name='lstm_3'))
    model.add(Dense(64, activation='relu', name='dense_1'))
    model.add(Dense(32, activation='relu', name='dense_2'))
    model.add(Dense(actions.shape[0], activation='softmax', name='output_layer'))

    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
    model.fit(X_train, y_train, epochs=100, callbacks=[tb_callback])
    model.save('my_model.keras')
    send_model_via_api(model, api_url)


def send_model_via_api(model, api_url):
    # Save the model architecture to JSON
    model_json = model.to_json()

    # Save the model weights to HDF5
    model.save_weights('model_weights.h5')

    # Send the model JSON and weights to the receiver
    files = {'model_json': ('model.json', model_json, 'application/json'),
             'model_weights': ('model_weights.h5', open('model_weights.h5', 'rb'), 'application/octet-stream')}
    
    response = requests.post(api_url, files=files)

    # Print the response from the receiver
    print(response.text)