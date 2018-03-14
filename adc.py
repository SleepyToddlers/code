'''
    This is a library that will control the adc and get measurements for
        1. Microphone: Snoring (2)
        2. Respiratory Belt: Resp Effort (1)
        3. Temperature Sensor: Nasal Effort (0)
        4. EKG: Heart Rate (3)

    Each of the variables will have their data stored in deques which will
    allow for filtering of the data at the end

    Need to determine the sample rate
'''

# Dependencies
from collections import deque
import Adafruit_ADS1x15


''' Setup Functions ----------------------------------- '''


''' --------------------------------------------------- '''

# Driver of the ADC
class ADC(object):

    # Initialize the class, default i2c add = 0x48
    def __init__(self):
        # Variable for adc
        self.device = Adafruit_ADS1x15.ADS1015() # Intiialize

        # Variables for the channels
        ekg = ''
        mic = ''
        blt = ''
        tmp = ''

    @property
    def heart_rate(self):
        return self.device.read_adc(3, gain=1)

    @property
    def nasal_temp(self):
        return self.device.read_adc(0, gain=1)

    @property
    def respiratory_belt(self):
        return self.device.read_adc(1, gain=1)

    @property
    def snore_mic(self):
        return self.device.read_adc(2, gain=1)

    def read_data(self):
        return (self.heart_rate, 
                self.nasal_temp, 
                self.respiratory_belt, 
                self.snore_mic)

