#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
from openvino.inference_engine import IECore

from iotdemo import FactoryController, MotionDetector

FORCE_STOP = False


def thread_cam1(q):
    # MotionDetector
    det = MotionDetector()

    # TODO: Load and initialize OpenVINO

    # HW2 Open video clip resources/factory/conveyor.mp4 instead of camera device.
    cap = cv2.VideoCapture("./resources/factory/conveyor.mp4")

    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam1 live", frame info
        q.put(("VIDEO:Cam1 live", frame))

        # TODO: Motion detect
        detect = dat.detect(frame)
        if detected is None:
            continue
            

        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.

        # TODO: Inference OpenVINO

        # TODO: in queue for moving the actuator 1

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q):
    # TODO: MotionDetector

    # TODO: ColorDetector

    # HW2 Open "resources/factory/conveyor.mp4" video clip
    cap = cv2.VideoCapture("./resources/factory/conveyor.mp4")
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put(("VIDEO:Cam1 live", frame))
        # TODO: Detect motion

        # TODO: Enqueue "VIDEO:Cam1 detected", detected info.

        # TODO: Detect color

        # TODO: Compute ratio
        print(f"{name}: {ratio:.2f}%")

        # TODO: Enqueue to handle actuator 2

    cap.release()
    q.put(('DONE', None))
    exit()


def imshow(title, frame, pos=None):
    cv2.namedWindow(title)
    if pos:
        cv2.moveWindow(title, pos[0], pos[1])
    cv2.imshow(title, frame)


def main():
    global FORCE_STOP

    parser = ArgumentParser(prog='python3 factory.py',
                            description="Factory tool")

    parser.add_argument("-d",
                        "--device",
                        default=None,
                        type=str,
                        help="Arduino port")
    args = parser.parse_args()

    # HW2 Create a Queue
    q = Queue()

    # HW2 Create thread_cam1 and thread_cam2 threads and start them.
    t1 = threading.Thread(target=thread_cam1, args(q, ), daemon=True)
    t2 = threading.Thread(target=thread_cam2, args(q, ), daemon=True)

    t1.start()
    t2.start()

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            # HW2 get an item from the queue. You might need to properly handle exceptions.
            # de-queue name and data
            try:
                event = q.get_nowait()
            except Empty:
                continue

            name, data = event

            # HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            if name.startswidth("VIDEO:"):
                imshow(name[6:], data)
            


            # TODO: Control actuator, name == 'PUSH'

            if name == 'DONE':
                FORCE_STOP = True

            q.task_done()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
