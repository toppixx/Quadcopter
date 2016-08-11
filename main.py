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



if __name__ == "__main__":
    #com1 = pyb.USB_VCP()  # A Virtual COM port
    mpu = MPU9250('y')
    mpu.sample_rate = 254
    mpu.accel_filter_range = 5
    mpu.gyro_filter_range = 2
    led1 = pyb.LED(1)
    led2 = pyb.LED(2)
    led3 = pyb.LED(3)
    led4 = pyb.LED(4)
    led3.on()
    kalmanX = kalmanFilter()
    led4.on()
    timeX = pyb.micros()
    kalmanY = kalmanFilter()
    timeY = pyb.micros()
    kalmanZ = kalmanFilter()
    timeZ =  pyb.micros()
    micropython.alloc_emergency_exception_buf(5)
    led4.on()
    #spiReset.low()
    pyb.delay(1)

    display = NextionUartDriver.NetiionDisplay(1,115200)
    #ownTimers.timerInterr()
    #ownTimers.initSysTime()
    #com1.write("Hello world!\n")

    while True:
        pyb.delay(20)
        display.addValueToWaveform("1", "0", "127")
        pyb.LED(4).toggle()
        #q = mpu.sensors()
        X = kalmanX.getAngle(math.atan2(mpu.accel.y, mpu.accel.z), mpu.gyro.x, timeX-pyb.micros())
        led2.off()
        led3.off()
        led4.off()

        #if (math.atan2(mpu.accel.x, mpu.accel.y)*180/math.pi) > 45:
        if (X*180/math.pi) > 0:
            led2.on()
        Y = kalmanY.getAngle(math.atan2(mpu.accel.x, mpu.accel.z), mpu.gyro.y, timeX-pyb.micros())

        if (Y*180/math.pi) > 0:
            led3.on()
        Z = kalmanZ.getAngle(math.atan2(mpu.accel.x, mpu.accel.y), mpu.gyro.z, timeX-pyb.micros())

        if (Z*180/math.pi) > 0:
            led4.on()
        #X = kalmanX.getAngle(math.atan2(2, 1), 30, timeX-pyb.micros())
        #com1.write('angle %.4f'%(1))
        #com1.write("angle test\n")
        timeX = pyb.micros()
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



