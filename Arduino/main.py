import time
import cv2
from utils import park
from kerasmodel.model import model_keras


def camera():
    # Webcam Video Capture
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # set W cam resolution
    # vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # set H cam resolution

    while True:
        # Return frames
        _, frame = vid.read()

        # Show video input
        cv2.imshow('input', frame)

        # Image classification with keras
        prediction = model_keras(frame)

        # If prediction > .95 use OCR to read licence plate
        if prediction > .4:
            park(prediction=prediction, frame=frame)

        # Click 'q' to finish
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close everything
    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    camera()
    # img = cv2.imread('plate.jpg')
    # predict_plate(prediction=0.99, frame=img)
