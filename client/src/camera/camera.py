import asyncio, cv2
from config import Config
import subprocess,time


STATIC_COMMAND = "/usr/bin/uvcdynctrl"

# ======================================================= #
# Contrôle des données de la caméra ===================== #
# ======================================================= #
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


# ======================================================= #
# Contrôle de l'orientation de la caméra ================ #
# ======================================================= #
timeout = 0.5

class CameraMove:

    def __init__(self):
        self.id = Config.Camera.ID
        self.x = 0
        self.y = 0
        self.move(0,0) # Initialisation de la caméra à (0,0)

    def wait(self, dt = timeout):
        time.sleep(dt)

    def command_make(self, instruction: str, value: str):
        subprocess.call(f"{STATIC_COMMAND} -d video{self.id} -s '{instruction}' -- '{value}' 2>/dev/null", shell=True)
        # return f"{STATIC_COMMAND} -d video{self.id} -s '{instruction}' -- '{value}'"
    
    def camera_down(self, value: int):
        if -32000 < value < 32000 : 
            self.command_make("Tilt, Relative",str(value))
            self.y += value
            return True
        return False
    
    def camera_left(self, value: int):
        if -32000 < value < 32000 : 
            self.command_make("Pan, Relative",str(value))
            self.x += value
            return True
        return False
    
    def reset_camera_down(self):
        self.command_make("Tilt, Reset","0")
        self.y = 0
    
    def reset_camera_left(self):
        self.command_make("Pan, Reset", "0")
        self.x = 0

    def reset(self):
        self.reset_camera_down()
        self.wait()
        self.reset_camera_left()
        self.wait()

    def demo(self):
        self.camera_down(1000)
        self.wait()
        self.reset_camera_down()
        self.wait()

        self.camera_down(-1000)
        self.wait()
        self.reset_camera_down()
        self.wait()

        self.camera_left(1000)
        self.wait()
        self.reset_camera_left()
        self.wait()

        self.camera_left(1000)
        self.wait()
        self.reset_camera_left()
        self.wait()


    def move(self, dd, dl):
        """ Bouger la caméra de manière relative.
        dd : down mvt, dl : left mvt.
        (0,0) est spécial : reset à l'origine. """
        if dd==0 and dl==0:
            self.reset()
        if dd != 0:
            self.camera_down(dd*500)
        if dl != 0:
            self.camera_left(dl*500)


