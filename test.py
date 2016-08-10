# main.py -- put your code here!
import pyb
#import ownTimers
from sens9250 import MPU9250
import micropython
import math
from Kalman import kalmanFilter
import NextionUartDriver

#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

"""Send a message from the PyBoard to whoever's at the other end of
   the USB cable.
"""

class test():
    def __init__(self):
        #com1 = pyb.USB_VCP()  # A Virtual COM port
        self.mpu = MPU9250('y')
        self.mpu.sample_rate = 254
        self.mpu.accel_filter_range = 5
        self.mpu.gyro_filter_range = 2
        self.led1 = pyb.LED(1)
        self.led2 = pyb.LED(2)
        self.led3 = pyb.LED(3)
        self.led4 = pyb.LED(4)
        self.led3.on()
        self.kalmanX = kalmanFilter()
        self.led4.on()
        self.timeX = pyb.micros()
        self.kalmanY = kalmanFilter()
        self.timeY = pyb.micros()
        self.kalmanZ = kalmanFilter()
        self.timeZ =  pyb.micros()
        micropython.alloc_emergency_exception_buf(5)
        self.led4.on()


        self.display = NextionUartDriver.NextionDisplay(1,115200)
        #self.ownTimers.timerInterr()
        #self.ownTimers.initSysTime()
        #self.com1.write("Hello world!\n")
    def run(self):

        while True:
                self.display.addValueToWaveform("1", "0", "127")
                pyb.LED(4).toggle()
                #self.q = mpu.sensors()
                self.X = self.kalmanX.getAngle(math.atan2(self.mpu.accel.y, self.mpu.accel.z), self.mpu.gyro.x, self.timeX-pyb.micros())
                self.led2.off()
                self.led3.off()
                self.led4.off()

                #if (math.atan2(self.mpu.accel.x, self.mpu.accel.y)*180/math.pi) > 45:
                if (self.X*180/math.pi) > 0:
                    self.led2.on()
                self.Y = self.kalmanY.getAngle(math.atan2(self.mpu.accel.x, self.mpu.accel.z), self.mpu.gyro.y, self.timeX-pyb.micros())

                if (self.Y*180/math.pi) > 0:
                    self.led3.on()
                self.Z = self.kalmanZ.getAngle(math.atan2(self.mpu.accel.x, self.mpu.accel.y), self.mpu.gyro.z, self.timeX-pyb.micros())

                if (self.Z*180/math.pi) > 0:
                    self.led4.on()
                #X = kalmanX.getAngle(math.atan2(2, 1), 30, timeX-pyb.micros())
                #com1.write('angle %.4f'%(1))
                #com1.write("angle test\n")
                self.timeX = pyb.micros()
                #kalmanY =# 0.0
                #timeY = pyb.micros()
                #kalmanZ = 0.0
                #timeZ =  pyb.micros()

                #phi = math.atan2(2*(q[0] * q[1]+q[2] * q[3]),1-2*q[1]*q[1]+q[2]*q[2])/math.pi*180 #So sieht der Prozeduraufruf aus
                #theta=math.asin(2*(q[0] * q[2]-q[3] * q[1]))/math.pi*180                                 #Einfach die Formeln nachgebildet
                #psi = math.atan2(2*(q[0] * q[3]+q[1] * q[2]),1-2*q[2]*q[2]+q[3]*q[3])/math.pi*180
                #mpu.accel.x
                #mpu.accel.y
                #mpu.accel.z

                #mpu.gyro.x
                #mpu.gyro.y
                #mpu.gyro.z

                #mpu.mag.x
                #mpu.mag.y
                #mpu.mag.z

if __name__ == "__main__":
    mainpro = main()
    mainpro.run()

