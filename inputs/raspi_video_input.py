# Copyright 2023 The MediaPipe Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main scripts to run gesture recognition."""

import argparse
import time
import logging

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from picamera2 import Picamera2

from inputs.video_input import VideoInput


class RaspiVideoInput(VideoInput):

    def __init__(self):
        self.picam2 = Picamera2()
        super(RaspiVideoInput, self).__init__()

    def start(self, controller):
        logging.getLogger("sevendots").debug(f'DEBUG EGV - video recognition launching')
        self.force_stop = False
        run_default(controller, self)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
stop = False


def run(model: str, num_hands: int,
        min_hand_detection_confidence: float,
        min_hand_presence_confidence: float, min_tracking_confidence: float,
        camera_id: int, width: int, height: int, controller, video_input: RaspiVideoInput) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
        model: Name of the gesture recognition model bundle.
        num_hands: Max number of hands can be detected by the recognizer.
        min_hand_detection_confidence: The minimum confidence score for hand
          detection to be considered successful.
        min_hand_presence_confidence: The minimum confidence score of hand
          presence score in the hand landmark detection.
        min_tracking_confidence: The minimum confidence score for the hand
          tracking to be considered successful.
        camera_id: The camera id to be passed to OpenCV.
        width: The width of the frame captured from the camera.
        height: The height of the frame captured from the camera.
    """

    # Start capturing video input from the camera
    video_input.picam2.configure(video_input.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
    video_input.picam2.start()

    # Visualization parameters
    fps_avg_frame_count = 10

    # Label box parameters
    recognition_result_list = []

    def save_result(result: vision.GestureRecognizerResult,
                    unused_output_image: mp.Image, timestamp_ms: int):
        global FPS, COUNTER, START_TIME

        # Calculate the FPS
        if COUNTER % fps_avg_frame_count == 0:
            FPS = fps_avg_frame_count / (time.time() - START_TIME)
            START_TIME = time.time()

        recognition_result_list.append(result)
        COUNTER += 1

    # Initialize the gesture recognizer model
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.GestureRecognizerOptions(base_options=base_options,
                                              running_mode=vision.RunningMode.LIVE_STREAM,
                                              num_hands=num_hands,
                                              min_hand_detection_confidence=min_hand_detection_confidence,
                                              min_hand_presence_confidence=min_hand_presence_confidence,
                                              min_tracking_confidence=min_tracking_confidence,
                                              result_callback=save_result)
    recognizer = vision.GestureRecognizer.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while True:
        image = video_input.picam2.capture_array()

        image = cv2.flip(image, 1)

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run gesture recognizer using the model.
        recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)

        if recognition_result_list:
            for hand_index, hand_landmarks in enumerate(
                    recognition_result_list[0].hand_landmarks):
                if recognition_result_list[0].gestures:
                    gesture = recognition_result_list[0].gestures[hand_index]
                    category_name = gesture[0].category_name
                    if controller is not None:
                        controller.process_command(category_name)
                    score = round(gesture[0].score, 2)
            recognition_result_list.clear()

        if video_input.force_stop:
            break

    video_input.picam2.stop()
    recognizer.close()


def run_default(controller, video_input: RaspiVideoInput):
    run('gesture_recognizer.task', 2, 0.5, 0.5, 0.5, 0, 640, 480, controller, video_input)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model',
        help='Name of gesture recognition model.',
        required=False,
        default='gesture_recognizer.task')
    parser.add_argument(
        '--numHands',
        help='Max number of hands that can be detected by the recognizer.',
        required=False,
        default=2)
    parser.add_argument(
        '--minHandDetectionConfidence',
        help='The minimum confidence score for hand detection to be considered '
             'successful.',
        required=False,
        default=0.5)
    parser.add_argument(
        '--minHandPresenceConfidence',
        help='The minimum confidence score of hand presence score in the hand '
             'landmark detection.',
        required=False,
        default=0.5)
    parser.add_argument(
        '--minTrackingConfidence',
        help='The minimum confidence score for the hand tracking to be '
             'considered successful.',
        required=False,
        default=0.5)
    # Finding the camera ID can be very reliant on platform-dependent methods.
    # One common approach is to use the fact that camera IDs are usually indexed sequentially by the OS, starting from 0.
    # Here, we use OpenCV and create a VideoCapture object for each potential ID with 'cap = cv2.VideoCapture(i)'.
    # If 'cap' is None or not 'cap.isOpened()', it indicates the camera ID is not available.
    parser.add_argument(
        '--cameraId', help='Id of camera.', required=False, default=-1)  # no usage with picamera2
    parser.add_argument(
        '--frameWidth',
        help='Width of frame to capture from camera.',
        required=False,
        default=640)
    parser.add_argument(
        '--frameHeight',
        help='Height of frame to capture from camera.',
        required=False,
        default=480)
    args = parser.parse_args()

    run(args.model, int(args.numHands), args.minHandDetectionConfidence,
        args.minHandPresenceConfidence, args.minTrackingConfidence,
        int(args.cameraId), args.frameWidth, args.frameHeight, None, None)
