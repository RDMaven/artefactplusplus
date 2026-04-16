import asyncio, cv2
from config import Config
import subprocess,time


STATIC_COMMAND = "/usr/bin/uvcdynctrl"

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

class CameraMove:

    def __init__(self):
        self.id = Config.Camera.ID


    def command_make(self, instruction: str, value: str):
        subprocess.call(f"{STATIC_COMMAND} -d video{self.id} -s '{instruction}' -- '{value}'", shell=True)
        # return f"{STATIC_COMMAND} -d video{self.id} -s '{instruction}' -- '{value}'"
    
    def camera_up(self, value: int):
        if -32000 < value < 32000 : 
            self.command_make("Tilt, Relative",str(value))
            return True
        return False
    
    def camera_right(self, value: int):
        if -32000 < value < 32000 : 
            self.command_make("Pan, Relative",str(value))
            return True
        return False
    
    def reset_camera_up(self):
        self.command_make("Tilt, Reset","0")
    
    def reset_camera_right(self):
        self.command_make("Pan, Reset", "0")

    def demo(self, slp=2):
        self.camera_up(1000)
        time.sleep(slp)
        self.reset_camera_up()
        time.sleep(slp)

        self.camera_up(-1000)
        time.sleep(slp)
        self.reset_camera_up()
        time.sleep(slp)

        self.camera_right(1000)
        time.sleep(slp)
        self.reset_camera_right()
        time.sleep(slp)

        self.camera_right(1000)
        time.sleep(slp)
        self.reset_camera_right()
        time.sleep(slp)


    def move_controls(self,x, y):
        if x==0 and y==0:
            self.reset_camera_right()
            self.reset_camera_up()
            return
        if y==0:
            self.camera_up(x*1000)
        else:
            self.camera_right(y*1000)
