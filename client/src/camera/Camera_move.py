import subprocess,time

STATIC_COMMAND = "/usr/bin/uvcdynctrl"

class Camera_move():

    def __init__(self, id: int):
        self.id = id
    
    def command_make(self, instruction: str, value: str):
        # return STATIC_COMMAND + " -d" + " video" + str(id) + " -s " + "'" + instruction + "'" + " -- " + "'" + value + "'"
        subprocess.call(f"{STATIC_COMMAND} -d video{self.id} -s '{instruction}' -- '{value}'", shell=True)
        return f"{STATIC_COMMAND} -d video{self.id} -s '{instruction}' -- '{value}'"
    
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
