import cv2
import time

def camera_feed(camera):
    """Video streaming generator function."""
    while not camera.stopped:
    # if camera.stopped:
    #     break
        frame = camera.read()
        ret, jpeg = cv2.imencode('.jpg', frame)

        # print("after get_frame")
        if jpeg is not None:
            time.sleep(0.016)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        else:
            print("frame is none")