import subprocess

STATIC_COMMAND = "/usr/bin/uvcdynctrl"

class Camera_move(id):
    def __init__(self, id: int):
        self.id = id
    def command_make(instruction: str, value :str, id: int):
        return STATIC_COMMAND + " -d" + " video" + str(id) + " -s " + "'" + instruction + "'" + " -- " + "'" + value + "'"
    def camera_up(self, id: int, value :int):
        if -32000 < value < 32000 : 
            self.command_make("Tilt, Relative",str(value), self.id)
            return True
        return False
    def camera_right(self, id: int, value :int):
        if -32000 < value < 32000 : 
            self.command_make("Pan, Relative",str(value), self.id)
            return True
        return False
    def reset_camera_up(self, id: int, value :int):
        self.command_make("Tilt, Reset","0",self.id)
    def reset_camera_right(self, id: int, value :int):
        self.command_make("Pan, Reset", "0", self.id)
