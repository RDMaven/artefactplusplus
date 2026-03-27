import asyncio, cv2
from config import Config

class Camera:

    def __init__(self):
        self.id = Config.Camera.ID
        self.fps = Config.Camera.FPS
        self.timeout_for_fps = round( 1/self.fps, 3)
        self.size = (640, 480)

        print(f"CAMERA - To achieve {self.fps} FPS, setting timeout to {self.timeout_for_fps}s")

        if Config.OS_IS_LINUX: # selon si on est sous linux, il faut cv.CAP_V4L2
            self.cap = cv2.VideoCapture(self.id, cv2.CAP_V4L2)
        else:
            self.cap = cv2.VideoCapture(self.id)

    def quit(self):
        self.cap.release()
        cv2.destroyAllWindows()

    async def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            await asyncio.sleep(0.01)
            return

        frame = cv2.resize(frame, self.size) #(320, 240)) # reduce size maybe TODO
        frame = cv2.flip(frame, 1) # flip image TODO enlever pour les robots (peut-être)
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70]) # reduce quality

        return buffer.tobytes()
