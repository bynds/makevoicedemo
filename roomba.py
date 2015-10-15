import serial, os


class Roomba():
    def __init__(self):
        self.arduinoIR = ArduinoIR()

    def turn(self, onOrOff):
        if onOrOff == 'on':
            self.turnOn()
        if onOrOff == 'off':
            self.turnOff()

    def turnOn(self):
        self.arduinoIR.executeArduinoIRCommand('turn on')

    def turnOff(self):
        self.arduinoIR.executeArduinoIRCommand('turn off')

    def clean(self):
        self.arduinoIR.executeArduinoIRCommand('clean')

    def goHome(self):
        self.arduinoIR.executeArduinoIRCommand('gohome')


class ArduinoIR():
    def listSerialPorts(self):
        if os.name == 'posix':
            self.available = []
            try:
                self.s = serial.Serial('/dev/ttyACM0', 9600)
                self.available.append('/dev/ttyACM0')
                self.s.close()
            except serial.SerialException:
                pass
            if len(self.available) == 0:
                raise Exception
            return self.available

    def executeArduinoIRCommand(self, command):
        try:
            self.serialPortsArray = []
            self.serialPortsArray = self.listSerialPorts()
        except:
            print "Is the arduino plugged in?"
        if len(self.serialPortsArray) == 1:
            self.ser = serial.Serial(self.serialPortsArray[0],
                                     timeout=5)  # open first serial port
            self.ser.write(command)  # write a string
            self.response = self.ser.readline()
            if self.response.endswith("is an unknown command"):
                print "The Arduino didn't understand our command"
                raise Exception
            print(self.response),
            self.ser.close()  # close port
