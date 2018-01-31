import Adafruit_ADS1x15
#import imu
import time

# Variable for sampling, says 128 sps
# For one min of data 128samples / 1 sec * 60 sec / 1 min 
MINUTES_TO_RECORD = 1
SAMPLES_PER_SECOND = 128

# Set up the sensors
adc_48 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1) # belt and temp
adc_49 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1) # snore and ekg
#belt 48 0
#temp 48 3
#snore 49 3
#ekg 49 0
#accel 

# Open the file
file = open('integration_testing.txt', 'w')

# Write to the file with the data
#for i in range(0, MINUTES_TO_RECORD*SAMPLES_PER_SECOND*60):

time_0 = time.time()

while True:
    # Get sensor data
	#accel = imu.get_sleep_position()
    belt = str(adc_48.read_adc_difference(0, gain=4))
    temp = str(adc_48.read_adc_difference(3, gain=4))
    snor = str(adc_49.read_adc(3, gain=1))
    ekg = str(adc_49.read_adc(0, gain = 1))

    # format output
    output = belt + ',' + temp + ',' + snor + ',' + ekg +  '\n'
    file.write(output)

    print(str(i))
    if time.time() - time_0 == MINUTES_TO_RECORD*60:
        break

file.close()
print('All done')