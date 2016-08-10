import NextionUartDriver
import pyb
import time

if __name__ == "__main__":
    led1 = pyb.LED(1)       
    led2 = pyb.LED(2)
    led3 = pyb.LED(3)
    led4 = pyb.LED(4)
    led4.on()
    display = NextionUartDriver.NetiionDisplay(1,9600)
    display.randset("1", "100")
    x=0
    i = 0
    while x==0:
        display.addValueToWaveform("1", "0", str(i))
        display.addValueToWaveform("1", "1", str(255-i))

        led3.on()
        time.sleep(0.02)
        led4.toggle()
        i = i+ 1
        if i == 255:
            i=0
        #x = x+1
        
import NextionUartDriver
display = NextionUartDriver.NetiionDisplay(1,115200)
display.sendRaw()
uart = pyb.UART(1, 9600)
uart.init(9600,  bits = 8,  parity = None,  stop = 1, timeout = 1)

#display.addValueToWaveform("1", "0", "127")
#display.clsColor("RED")

