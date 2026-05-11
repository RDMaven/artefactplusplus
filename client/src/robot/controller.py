#! /usr/bin/env python3
import serial
from threading import Thread
from time import sleep

class Reference:
    def __init__(self, odom: list, is_relative = False):
        """ Si is_relative est vrai, alors on récupèrera toujours seulement le nombre de ticks depuis le dernière appel. 
        Si faux, ils seront relatifs aux nombre de ticks à la création de la référence."""
        self.l0, self.r0 = odom
        if is_relative:
            self.l, self.r = odom
        else:
            self.l = 0
            self.r = 0
        
        self.update = (lambda odom: self.update_non_relative(odom)) if not is_relative else (lambda odom: self.update_relative(odom))

    def update_non_relative(self, odom):
        tl, tr = odom
        self.l = tl-self.l0
        self.r = tr-self.r0
        # print(f"ref update : odom={odom} et l0={self.l0}, r0={self.r0} -> l={self.l}, r={self.r}")

    def update_relative(self, odom):
        tl, tr = odom
        self.l = tl - self.l
        self.r = tr - self.r
        

class WifiBot:
    def __init__(self, serPath):
        # open the serial port
        self.serialPort = serial.Serial()
        self.serialPort.baudrate = 19200
        self.serialPort.port = serPath
        self.serialPort.bytesize = serial.EIGHTBITS
        self.serialPort.parity   = serial.PARITY_NONE
        self.serialPort.stopbits = serial.STOPBITS_ONE
        self.serialPort.xonxoff  = False
        self.serialPort.ctsrts   = False
        self.serialPort.dsrdtr   = False
        self.serialPort.open()
        # command buffer
        # always starts with 0xff and payload+crc is 7 bytes
        self.cmd = bytearray(9)
        self.cmd[0] = 0xFF
        self.cmd[1] = 7
        # defaults ?
        #             con. L
        #                   con. R
        #                         sensor on
        self.cmd[6] = 1<<7 | 1<<5 | 1<<0;
        self.updateCrc()
        # robot state
        self.speedL   = 0
        self.IrRF     = 0
        self.IrLB     = 0
        self.OdomL    = 0
        self.speedR   = 0
        self.IrLF     = 0
        self.IrRB     = 0
        self.OdomR    = 0
        self.BatLevel = 0
        self.Current  = 0
        self.Version  = 0xff
        # threads
        self.started = False

    def start(self):
        cmdThread = Thread(target=self.runSendCmd      ,args=(), daemon=True)
        staThread = Thread(target=self.runUpdateStatus ,args=(), daemon=True)
        self.started = True
        cmdThread.start()
        staThread.start()

    def stop(self):
        self.started = False

    @staticmethod
    def modbus_crc16(t:bytearray):
        crc =  0xffff
        poly = 0xA001
        for b in t:
            crc = crc ^ b
            for i in range(8):
                par = crc%2
                crc = crc >> 1
                if (par): crc = crc ^ poly
        return crc

    def updateCrc(self):
        crc = self.modbus_crc16(self.cmd[1:7])
        self.cmd[7] = crc & 0xff
        self.cmd[8] = (crc>>8) & 0xff

    def __setSpeed(self, v:int, p:int):
        self.cmd[p] = v & 0xff
        self.cmd[p+1] = (v>>8) & 0xff
        self.updateCrc()

    def __set_Ctrl(self, forward:bool, p:int):
        if forward:
            self.cmd[6] = self.cmd[6] | (1<<p)
        else:
            self.cmd[6] = self.cmd[6] & ~(1<<p)
        self.updateCrc()

    def setLeftSpeed(self, v:int):
        self.__setSpeed(v,2)

    def setLeftForward(self, forward:bool):
        self.__set_Ctrl(forward,6)

    def setRightSpeed(self, v:int):
        self.__setSpeed(v,4)

    def setRightForward(self, forward:bool):
        self.__set_Ctrl(forward,4)

    def sendCmd(self):
            self.serialPort.write(self.cmd)

    def updateStatus(self):
        """
        This method updates the robot state from the periodic frame sent by the
        robot through its serial port.
        Each frame starts with 255, but 255 is a legal value within a frame, so
        we read a longer frame that will contain two consecutive frames.  Once
        found, we compute the checksum to verify that we have a correct frame.
        The input buffer is systematically reset, to  avoid having old
        buffered data.
        """

        self.serialPort.reset_input_buffer()
        rawresp = self.serialPort.read(43)
        for i in range(20):
            if rawresp[i] == 0xFF and rawresp[i+22] == 0xFF:
                resp = rawresp[1+i:1+i+21]
                # Last two elements are the sent checksum
                crcR = resp[-1]<<8 | resp[-2]
                # compute the checksum locally on the 19 first elements
                crc = self.modbus_crc16(resp[0:-2])
                if crc == crcR :
                    self.speedL   = resp[1]<<8 | resp[0]
                    # speed is 16-bit signed
                    if(self.speedL >= 0x8000):
                        self.speedL = self.speedL - 0x10000
                    self.BatLevel = resp[2]
                    self.IrRF     = resp[3]
                    self.IrLB     = resp[4]
                    self.OdomL    = resp[8]<<24 | resp[7]<<16 | resp[6]<<8 | resp[5]
                    self.speedR   = resp[10]<<8 | resp[9]
                    if(self.speedR >= 0x8000):
                        self.speedR = self.speedR - 0x10000
                    self.IrLF     = resp[11]
                    self.IrRB     = resp[12]
                    self.OdomR    = resp[16]<<24 | resp[15]<<16 | resp[14]<<8 | resp[13]
                    self.Current  = resp[17]
                    self.Version  = resp[18]

    def printStatus(self):
        # TODO: 1/2 --> Front/Back
        s = f"""
            Global:
                Version       : {self.Version:02x}
                Battery Level : {self.BatLevel}
                Current       : {self.Current}
            Left:
                Speed         : {self.speedL}
                Odometry      : {self.OdomL}
                Sensor Fr     : {self.IrLF}
                Sensor Bk     : {self.IrLB}
            Right:
                Speed         : {self.speedR}
                Odometry      : {self.OdomR}
                Sensor Fr     : {self.IrRF}
                Sensor Bk     : {self.IrRB}
        """
        print(s)

    def runSendCmd(self):
        """Continuously send the command frame"""
        while self.started:
            self.sendCmd()
            sleep(0.100)

    def runUpdateStatus(self):
        """Continuously update status"""
        while self.started:
            self.updateStatus()
            sleep(0.200)


    def runInteractive(self):
        cur_speed=150
        if not self.started:
            self.start()
            sleep(0.5)

        while 1:
            key = input().lower()
            if key == 'z':
                self.setRightSpeed(cur_speed)
                self.setLeftSpeed(cur_speed)
                self.setLeftForward(True)
                self.setRightForward(True)
            elif key == 's':
                self.setRightSpeed(cur_speed)
                self.setLeftSpeed(cur_speed)
                self.setLeftForward(False)
                self.setRightForward(False)

            elif key == 'q':
                self.setLeftForward(True)
                self.setRightForward(True)
                self.setRightSpeed(cur_speed)
                self.setLeftSpeed(0)
            elif key == 'd':
                self.setLeftForward(True)
                self.setRightForward(True)
                self.setRightSpeed(0)
                self.setLeftSpeed(cur_speed)

            elif key == 'r':
                self.setRightSpeed(cur_speed)
                self.setLeftSpeed(cur_speed)
            elif key == 'f':
                self.setRightSpeed(0)
                self.setLeftSpeed(0)
            elif key == 'x':
                self.stop()
                break

    def forceStart(self):
        if not self.started:
            print("Robot was not started, starting.")
            self.start()
            self.setLeftSpeed(1) # TODO try with 0
            self.setRightSpeed(1)

    def getOdom(self, is_setup=False):
        if is_setup:
            self.forceStart()
            sleep(0.5)
        return [self.OdomL, self.OdomR]

    def updateOdomReference(self, ref: Reference):
        ref.update(self.getOdom())
        

if __name__ == "__main__":
   wb = WifiBot("/dev/ttyUSB0")
   wb.start()
   sleep(1)

   # wb.runInteractive()
   # sleep(0.5)
   ### wb.setRightForward(True)
   ### wb.printStatus()
   ### q = input("start")
   ### wb.setRightSpeed(0)
   ### q = input("stop?")
   ### wb.setRightSpeed(0)
   ### sleep(0.5)
   ### wb.printStatus()
   
   print("--------------------------")
   wb.printStatus()
   print("--------------------------")
   wb.runInteractive()
#    wb.setLeftSpeed(200)
#    wb.setRightSpeed(200)
#    wb.setLeftForward(True)
#    wb.setRightForward(False)
#    sleep(3)
   wb.printStatus()
   print("--------------------------")

#    wb.setLeftSpeed(40)
#    sleep(2)
#    wb.printStatus()
#    print("--------------------------")
#    wb.setRightSpeed(40)
#    sleep(2)
#    wb.printStatus()
#    print("--------------------------")
#    wb.setLeftForward(True)
#    sleep(2)
#    wb.printStatus()
#    print("--------------------------")
#    wb.setRightForward(True)
#    sleep(2)
#    wb.printStatus()
#    print("--------------------------")
   wb.stop()

