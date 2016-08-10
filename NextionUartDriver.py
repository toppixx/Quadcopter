# Copyright (C) 2016 Tobias Faller, All rights reserved.
# This software may be distributed and modified under the terms of the GNU
# General Public License version 2 (GPL2) as published by the Free Software
# Foundation and appearing in the file GPL2.TXT included in the packaging of
# this file. Please note that GPL2 Section 2[b] requires that all works based
# on this software must also be made publicly available under the terms of
# the GPL2 ("Copyleft").
# Contact information
# -------------------


'''
The NextionUArtDriver is a library for the Nextion LCD Display controlled by a pyboard.
'''
# with NETION marked comments reffer to http://wiki.iteadstudio.com/Nextion_Instruction_Set#Nextion_HMI:_System_Variables_List

from  pyb import UART
class NetiionDisplay():
    '''
    NetiionDisplay constructor arguments
    1. UART chose the UART from the pyboard
    '''


    def __init__(self, Uart = 1,  Baudrate = 115200):

        self.uart = UART(Uart, Baudrate)
        self.uart.init(Baudrate,  bits = 8,  parity = None,  stop = 1)
        self.endCmdff = ("%c%c%c"%(0xff, 0xff, 0xff))

    def sendRaw(self,  data=""):
        '''sends a string as raw data'''
        data = data + self.endCmdff
        return self.uart.write(data)
        
    def readRaw(self):
        '''reads a string as raw data'''
        cnt = 0
        data = []
        file = open('log/log.txt', 'w')
        
        data.append(self.uart.read())
        x=0
        file.write(str(data[x]))
        while cnt < 3:
            data.append(self.uart.read())
            if data[len(data)-1]== 0xff:
                cnt = cnt + 1
            else:
                cnt = 0
            x=x+1
            file.write(data[x])
        file.close()    
        return data
        
    def readComandsBack(self):            
        '''
        Table 1: serial l instruction execution success or failure notification format

        1.Only when the system variable bkcmd is not zero will return instruction execution succeed or fail data, bkcmd defaults to 0 after each power on, which means it does not return the result of instruction execution.

        2.The code of the source file is not affected by bkcmd when software is under editing, the error data will be returned when there is an execution error, and the error data will not be returned when execute success.

        3.The returned data is ended with three bytes of “0XFF 0XFF 0XFF”.
        Byte 	Meaning 	                Format
        0X00 	                            Invalid instruction 	    0X00+End
            
        0X01   	Successful execution of instruction 	0X01+End

        0X03 	Page ID invalid 	0X03+End

        0X04 	Picture ID invalid 	0X04+End

        0X05 	Font ID invalid 	0X05+End
        
        0X11 	Baud rate setting invalid 	0X11+End
                Baud rate supported by the device including:2400 4800 9600 19200 38400 57600 115200
        0X12 	Curve control ID number or channel number is invalid 	0X12+End
        
        0X1A 	Variable name invalid 	0X1A+End
        
        0X1B 	Variable operation invalid 	0X1B+End
                For example, when txt attribute of text component t0 is assigned, it should be written as t0.txt=“abc” It is wrong if you write t0.txt=abc.
                For another example, the val attribute of progress bar j0 should be numerical, so it should be written as j0.val=50; it will be wrong if you write j0.val=“50” or j0.val=abc.
        
        0X1C 	Failed to assign 	0X1C+End

        0X1D 	Operate PERFROM failed 	0X1D+End

        0X1E 	Parameter quantity invalid 	0X1E+End

        0X1F 	IO operate failed 	0X1F+End


        Table 2: other data return format

        1.The returned data is end with three bytes of “0XFF 0XFF 0XFF”.

        2.The following data’s return does not be affected by bkcmd.
        
        data 	Meaning 	            Format
        0X65 	Touch event return data 	0X65+Page ID+Component ID+TouchEvent+End
        Definition of TouchEvent: Press Event 0x01, Release Event 0X00)
        Instance: 0X65 0X00 0X02 0X01 0XFF 0XFF 0XFF'
        Meaning: Page 0, Button 2, Press
        0X66 	Current page ID number returns 	0X66+Page ID+End
        The device returns this data after receiving “sendme” instruction)
        
        Instance: 0X66 0X02 0XFF 0XFF 0XFF
        Meaning: Current page ID is 2
        0X67 	Touch coordinate data returns 	0X67++ Coordinate X High-order+Coordinate X Low-order+Coordinate Y High-order+Coordinate Y Low-order+TouchEvent State+End
        When the system variable “sendxy” is 1, return this data at TouchEvent occurring
        Definition of TouchEvent: Press Event 0x01, Release Event 0X00
        
        Instance: 0X67 0X00 0X7A 0X00 0X1E 0X01 0XFF 0XFF 0XFF
        Meaning: Coordinate (122,30), Touch Event: Press
        0X68 	Touch Event in sleep mode 	0X68++Coordinate X High-order+Coordinate X Low-order+Coordinate Y High-order+Coordinate Y Low-order+TouchEvent State+End
        When the device enters sleep mode, return this data at TouchEvent occurring
        Definition of TouchEvent: Press Event 0x01, Release Event 0X00
        
        Instance: 0X68 0X00 0X7A 0X00 0X1E 0X01 0XFF 0XFF 0XFF
        Meaning: Coordinate (122,30), Touch Event: Press
        0X70 	String variable data returns 	0X70+Variable Content in ASCII code+End
        When the variable obtained through get command is string type, return this data
        
        Instance: 0X70 0X61 0X62 0X63 0XFF 0XFF 0XFF
        Meaning: Return the string data: “abc”
        0X71 	Numeric variable data returns 	0X71+variable binary data(4 bytes little endian mode, low in front)+End
        When the variable obtained by get command is value, this data returns.
        
        Instance:0X71 0X66 0X00 0X00 0X00 0XFF 0XFF 0XFF
        Meaning:return value data:102
        0X86 	Device automatically enters into sleep mode 	0X86+End

        Only when the device automatically enters into sleep mode will return this data. If execute serial command “sleep = 1” to enter into sleep mode, it will not return this data.
        0X87 	Device automatically wake up 	0X87+End

        Only when the device automatically wake up will return this data. If execute serial command “sleep=0” to wake up, it will not return this data.
        0X88 	System successful start up 	This data is sent after a successful power-on initialization on the device
        0X89 	Start SD card upgrade 	This data is sent after the device power on and detect SD card, and then enter upgrade interface
        OXFE 	Data transparent transmit ready 	The device will enter into transparent transmission data initialization mode after receiving data transparent transmission instruction. Data will be sent once the initialization is completed, which means it has entered into data transparent transmission mode and start to transparent transmit data. 
        '''
        return self.readRaw()


    def setPage(self,  PageID = "" ):
        '''NETION
         setPage(PageID = "p0" )        #sets selected page to front 

        PageID: Page ID or Page Name 
        This funktion sets the selected page to the front
        '''
        self.sendRaw("page %s" %(PageID))
        
    def refreshcmpID(self, ComponentID = "0"):
        '''NETION 
        ComponentID: component ID or component name 
        
        refreshcmpID(ComponentID = "b0")        #refreshes the selected Component
        
        The default loading mode is automatically load when you create and edit a component in Nextion Editor. If set it as manually load, you should use ref command to load the component. Or when the component is covered by the other components, you can use this command to refresh the covered component. 
            
        ref 0: refresh all components of the current page 
        If you refresh one of the components,the component will be on the first top,but covers the others.Use this command "ref 0" will be work well. 
        '''
        self.sendRaw("ref %s" %(ComponentID))
 
    def refObJname(self, Jname = "0"):
        '''NETION 
        Jname: component name 
        
        refObJname(Jname = "t0")        #the component starts to auto refresh
        
        1. Component auto refresh when attribute changes only valid for those attributes in green bold font. The other attributes not in this format can only be refreshed and displayed by the command of ref.

        2.When creating a component in Nextion editor, the default loading mode is auto loading. When the loading mode is set as manual loading, it requires to use ref to load. When the component is sheltered by GUI command mapping, or when the component is sheltered by other manual loading components, you can use ref to refresh the component. 
        '''
        self.sendRaw("ref %s" %(Jname))
 
 
    def refStop (self):
        '''NETION 
        stop refreshing screen 
        
        refStop()       #stops refreshing screen
        
        1.If you do not want to see the whole waveform flow progress, rather, you want to view the whole waveform all at once, you can stop refreshing the screen and refresh it when all adopted points being passed through.

        2.Once stop refreshing the screen, all other commands and responded attribute assign operations will still run normally, but the components on the screen will not auto-refresh, neither will any changes in component attributes be refreshed and displayed on the screen(the changes are valid). When the device receive the command ref_star, those changes will be immediately refreshed and displayed on the screen (on condition that the changes are made from the attributes in green bold font).

        3.When stop refreshing the screen, ref command will still be executed. Besides, all GUI drawing instructions such as draw point, draw line will still be executed and any changes will be immediately displayed. 
        '''
        self.sendRaw("ref_stop")
    
    def refStar (self):
        '''NETION 
        recover refreshing screen 
        
        refStar()       #recovers refreshing screen
        
        This command should be used with ref_stop command. 
        '''
        self.sendRaw("ref_star")
 
    def getAtt(self,  Attribute = ""):
        '''NETION 
        return the attribute of a object
    
        getAtt(Attribute = "t0.txt")      #return t0's txt value
        
        1. When returned value is a string, the returned data is 0X70+ASCII code+0xff 0xff 0xff.

        2. When returned value is numerical, returned data is 0X71+4 byte binary data+0xff 0xff 0xff. The data storage mode is little-endian mode (namely, low-order in front, and high-order at back).

        3. The specific returning format of data, please refer to the table: Format of Device Return Data   
        '''
        self.sendRaw("set %s" %(Attribute))

    def sendme(self):
        '''NETION 
        If you want the page auto-send pageID every refresh, simply enter sendme in page initialize event. 
        ''' 
        self.sendRaw("sendme")
        
    def cov(self, From = "", To = "",  Length = "0"):
        '''NETION 
        cov("att1", "att2", Length = "lenth")       #converts the value from one objekt to another

        att1: source variable
        att2: target variable
        lenth: length of the string(0 is automatic length, not- 0 is fixed length)          
        cov(From = "h0.val", To = "t0.txt", 0)
        
        1.lenth always represents the length of the string, when the value converts into string, it is the length of target variable; when the string converts into value, it is the length of source variable.

        2. If the target variable and source variable are of the same type, the conversion failed.      
        '''
        self.sendRaw("cov %s,%s,%d" %(From,  To,  Length)) 

 
    def touchJ(self): 
        '''NETION 
        calibrate touch 
        All the devices have been calibrated before packing from the factory, this command is not needed under normal circumstances 
        '''
        self.sendRaw("touch_j") 
 
    def visisble(self, Component = "255",  State = "1"):
        '''NETION 
        vis;hide/show component
        
        Component: component name or component ID 
        State: state("0" or "1")
        
        visisble(Component = "b0", State = "0")     #hide component b0
        visisble(Component = "1", State = "1")      #show the component whose ID is 1

        1.The first parameter 255 means all components in current page, for example: vis 255,0 (hide all components in current page); vis 255,1 (show all components in current page). 
        '''
        self.sendRaw("vis %s,%s" %(Component, State)) 

    def clearTouch(self):  
        '''NETION 
        clearTouch()        #disables the touch of the active area
        
        When you use this command, all touch areas you set in the current page will neither be valid, nor automatically be identified.Until you use the "page" command, the touch areas can be reloaded. 
        '''
        self.sendRaw("cle_c") 

    def setTouchOfObj(self, Component = "255", State = "1"):
        '''NETION 
        Enable/disable component touch function
        Component: component name or component ID
        State: state("0" or "1")

        setTouchOfObj(Component = "b0", State = "0")      #component b0 touch invalid
        setTouchOfObj(Component = "1", State = "1")       #component of ID 1 touch valid
        
        1.The first parameter 255 means all components in current page, for example: setTouchOfObj( Component = "255", State = "0" (all components in current page touch invalid); tsw 255, 1 (all components in current page touch valid). 
        '''
        self.sendRaw("tsw %s,%s"%(Component, State)) 
        
    def comStop(self):
        '''NETION 
        This command is used for pausing the execution of serial port commands, but note that the device will continue receiving the commands and store them in the buffer. Until receiving "com_star" commands, the device will execute the rest commands that store in the buffer.
        
        comStop()
        
        When using this command to pause the execution, please make sure whether the buffer size and the maximum capacity of command queue can store all the commands you need. You will find these two parameter in Nextion Hardware manual. 
        '''
        self.sendRaw("com_stop")
        
    def comStart(self):
        '''NETION 
        After receiving this command, the device will execute all the commands that store in the buffer.
        
        comStart()
        
        When using this command to recover the execution, please make sure whether the buffer size and the maximum capacity of command queue can store all the commands you need. You will find these two parameter in Nextion Hardware manual. 
        '''
        self.sendRaw("com_star")

    def randset(self, MinVal = "1",  MaxVal = "100"):
        '''NETION 
        randset: set random value range
        randset minval, maxval
        MinVal: minimum value
        MaxVal: maximum value

        ranset(low = "1",high = "100")  set current value randomly generated from 1 to 100

        1. You should use randset to set random value generated range beforehand. Without setting randset, the value range will be 0~4294967295 by default. Aftering setting randset, you will get a new random value within the preset range every time you run rand

        2. The range set by randset keeps valid unless the device being reboot or reset. 
        '''
        self.sendRaw("com_star %s,%s" %(MinVal, MaxVal))

    def codeC(self):
        '''
        Clear the commands that is stored in the buffer but not executed. 
        '''
        self.sendRaw("code _c")

    
    # print
    #printh 
    #are only used by the Display
    def addValueToWaveform(self,  ComponentID = "0",  Chanel = "0",  Value = "127"):
        '''NETION 
        ComponentID Waveform component ID
        Chanel: Waveform component channel number
        Value: value (maximum 255, minimum 0)

        addValueToWaveform(ComponentID = "1", Chanel = "0", Value = "30")  #add data 30 to channel 0 of the Waveform component which ID number is 1
        addValueToWaveform(ComponentID = "1", Chanel = "1", Value = "50")  #add data 50 to channel 1 of the Waveform component which ID number is 1

        1.Waveform component only support 8-bit values, 0 minimum, 255 maximum.

        2.Each page supports up to four Waveform components, each Waveform component supports up to four channels. It supports continuously pass through data, the component will auto-flow and display the value. It supports to change attributes during passing through data, such as change the background color or foreground color for each channel during the process. 
        '''
        self.sendRaw("add %s,%s,%s" %(ComponentID, Chanel, Value))

    def addValueToWaveformTroughtput(self,  ComponentID = "0",  Chanel = "0",  NumerOfValues = "10"):
        '''NETION 
        Waveform data pass through command
          
        addValueToWaveformTroughtput(cmpID, ch, qyt)
        ComponentID: waveform component ID
        Chanel: channel number in waveform component
        NumerOfValues: adopted point quantity of the data

        addt 1, 0, 100  #waveform component whose ID is 1 enter into data pass through mode, pass through adopted point quantity is 100

        1.Waveform component only support 8-bit values, 0 minimum, 255 maximum. Single pass through is 1024 bits maximum.

        2.After sending waveform data pass through command, it will take some time to get the device responded and started passing through values. This period takes about 5ms(it will take longer if there are other commands to be executed in the buffer zone before executing data pass through command). Following this period, it will send a data pass through ready data(0XFE+Terminator) to user, then it will start sending pass through data. The data being passed are only hexadecimal numbers. It recovers to command receiving state only after the device has adopted specified data.

        3.Waveform will not refresh until specified data has been passed through completely. 
        '''
        self.sendRaw("addt %s,%s,%s" %(ComponentID, Chanel, NumerOfValues))

    def reset(self):
        '''resets the display'''
        self.sendRaw("reset")
        



#----------------------------------------------------------------------------------------
#Classification II: GUI Designing Command
#----------------------------------------------------------------------------------------

    def clsColor(self, ColorByName = "",  ColorByValue = 0):
        ''''
        Note: When you can’t realize some special GUI designing in Nextion Editor, you can use some GUI commands to make it happen. Generally, the controls in Nextion editor can satisfy your GUI designing demand.
        cls color
        Sets the whole screen to the selected color
        
        clsColor(self, ColorByName = "BLACK")       #sets the screen to black
        clsColor(self,  ColorByValue = 65535)           #sets the screen to white
        
        You can define color by name or by value
        Name is more prior
        
        Names and also there Values are all other values (0-65535) are possible: Black = 0 White is 65535
        RED 	63488 	
        BLUE 	31 	
        GRAY 	33840 	
        BLACK 	0 	
        WHITE 	65535 	
        GREEN 	2016 	
        BROWN 	48192 	
        YELLOW 	65504 	 
        
        '''
        if ColorByName != "":
            self.sendRaw("cls %s" %(ColorByName))
        else : 
            self.sendRaw("cls %d" %(ColorByValue))
            


    
