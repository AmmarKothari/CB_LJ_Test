import u12
import time
import numpy
import logging
import sys
#import matplotlib.pyplot as plt
print("Import Complete")


def init_setup():
    ###########PINS USED#############
    global SevenFivePin, TwentyFourPin, LJ1, num_readings
    SevenFivePin = 0 #AI0
    TwentyFourPin = 1 #AI1
    print("Pins Set")
    #########RESISTORS###############
    R_TF_1 = 1000
    R_TF_2 = 1000
    R_S_1 = 1000
    R_S_1 = 1000
    R_LJ = 46000
    REff = lambda R_1, R_2: return 1/(1/R_1 + 1/R_2)
    R_TF_E = REff(R_LJ, R_TF_2)
    R_S_E = REff(R_LJ, R_S_2)
    global R_TF_Ratio, R_S_Ratio
    R_TF_Ratio = R_TF_E/(R_TF_1 + R_TF_E)
    R_S_Ratio = R_S_E/(R_S_1 + R_S_E)
    #########GENERAL CONSTANTS#########
    num_readings = 10
    #####LOG TO FILE#####
    log_file_name = ""
    #logging.basicConfigicConfig(filename=log_file_name, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    ####send to terminal####
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    ########Initializing Lab Jack#######
    try:
        LJ1=u12.U12() #labjack object
        print(LJ1)
        print("Success!")
    except Exception, e:
        print("THIS IS NOT WORKING!")
        print(e)
        sys.exit()
        #LJ1.open()
    LJ1_ID = LJ1.devid() #labjack id should be zero
    if LJ1_ID != 0:
    	#    print("There may be multiple Lab Jacks Connected.  BEWARE!")
    return LJ1_ID 
    #verify serial number?
    #verify only one lab jack connected


def Reset_LabJack():
    logging.debug("Resetting LabJack")
    idnum = 0 #error code for lab jac
    errorString = 0
    global LJ1
    try:
        LJ1.rawReset()
        sleep_time = 5
        for i in range(1,sleep_time+1):
            time.sleep(1)
        print("The handle for the labJack is: %s" %LJ1.handle)
        if LJ1.handle is None:
        	LJ1.open()
        print("Success: Lab Jack Restarted")
    except u12.U12Exception:
        print("Lab Jack Error: %s" %idnum)
    return idnum

def SevenFiveVCheck():
    global SevenFivePin, R_S_Ratio
    logging.debug("7.5V Voltage Check")
    AverageVoltage = MeasureVoltage(SevenFivePin) / R_S_Ratio #Voltage read with initialized divider. Adjust to find CB output.
    Result = VoltageAcceptable(AverageVoltage, 7, 8)
    return(AverageVoltage, Result)

def TwentyFourLowVCheck():
    global TwentyFourPin, R_TF_Ratio
    logging.debug("24V Low Voltage Check")
    AverageVoltage = MeasureVoltage(TwentyFourPin) / R_TF_Ratio #Voltage read with initialized divider. Adjust to find CB output.
    Result = VoltageAcceptable(AverageVoltage, -.1, .1)
    return(AverageVoltage, Result)

def VoltageCheck(input_pin, avg_V, LL_V, UL_V):
    AverageVoltage = MeasureVoltage(input_pin)
    Result = VoltageAcceptable(AverageVoltage, LL_V, UL_V)

def VoltageAcceptable(AverageVoltage, LL, UL):
	#Check to see if voltage is within limits
	#Could do this at GUI
    if LL<=AverageVoltage<=UL:
        print("Voltage is Acceptable")
        result = 1
    else:
        print("Voltage is not Acceptable")
        result = 0
    return(result)
        
def MeasureVoltage(pin_number):
    #Pass pin number for analog voltage reading
    global logging
    global LJ1
    VoltageReadings = []
    for i in range(0,num_readings): #measure multiple times and average
        Output = LJ1.eAnalogIn(channel=pin_number, gain=0)
        logging.debug("Measured Voltage is: %s" %Output['voltage'])
        VoltageReadings.append(Output['voltage'])
    AverageVoltage = float(sum(VoltageReadings)/max(len(VoltageReadings),1)) #ensures there was at least one reading
    print("Average Voltage: %s" %AverageVoltage)
    StdVoltage = numpy.std(VoltageReadings)
    print("Standard Deviation of Voltage: %s" %StdVoltage)

def test_Sequence():
    global LJ1
    init_setup()
    print("Labjack Initialized")
    #Assuming only 1 lab jack is connected
    #Reset labjack
    #Reset_LabJack()
    #Check for 7.5V
    SevenFiveVCheck()
    #Check for 8V (24 low voltage)
    TwentyFourLowVCheck()


test_Sequence()
